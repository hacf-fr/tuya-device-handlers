"""Common utility functions for Tuya quirks."""

from __future__ import annotations

from enum import StrEnum
import json
import logging
from typing import TYPE_CHECKING

from .const import TuyaDPType
from .models import (
    TuyaDataPointDefinition,
    TuyaEnumTypeDefinition,
    TuyaIntegerTypeDefinition,
)

if TYPE_CHECKING:
    from tuya_sharing import CustomerDevice  # type: ignore[import-untyped]

_LOGGER = logging.getLogger(__name__)


def parse_enum[T: StrEnum](enum_class: type[T], value: str | None) -> T | None:
    """Parse a string to an enum member.

    Return None if value is None or if the value does not correspond to any
    enum member.
    """
    if value is None:
        return None
    try:
        return enum_class(value)
    except ValueError:
        return None


_DPTYPE_MAPPING: dict[str, TuyaDPType] = {
    "bitmap": TuyaDPType.BITMAP,
    "bool": TuyaDPType.BOOLEAN,
    "enum": TuyaDPType.ENUM,
    "json": TuyaDPType.JSON,
    "raw": TuyaDPType.RAW,
    "string": TuyaDPType.STRING,
    "value": TuyaDPType.INTEGER,
}


def parse_dp_type(current_type: str) -> TuyaDPType | None:
    try:
        return TuyaDPType(current_type)
    except ValueError:
        # Sometimes, we get ill-formed DPTypes from the cloud,
        # this fixes them and maps them to the correct DPType.
        return _DPTYPE_MAPPING.get(current_type)


def get_dp_definition(
    device: CustomerDevice,
    dp_code: str | None,
    *,
    prefer_function: bool = False,
) -> TuyaDataPointDefinition | None:
    """Find a matching DPType type information for this device DPCode."""
    if dp_code is None:
        return None

    lookup_tuple = (
        (device.function, device.status_range)
        if prefer_function
        else (device.status_range, device.function)
    )

    for device_specs in lookup_tuple:
        if current_definition := device_specs.get(dp_code):
            if current_type := parse_dp_type(current_definition.type):
                return TuyaDataPointDefinition(
                    dp_code=dp_code,
                    dp_type=current_type,
                    specs=current_definition,
                )

    return None


def parse_dp_enum_definition(
    definition: TuyaDataPointDefinition,
) -> TuyaEnumTypeDefinition | None:
    if definition.dp_type != TuyaDPType.ENUM:
        _LOGGER.warning(
            f"Failed to parse enum definition: expected dp type ENUM, got {definition.dp_type}"
        )
        return None
    if TYPE_CHECKING:
        assert isinstance(definition.specs.values, str)

    parsed = json.loads(definition.specs.values)
    return TuyaEnumTypeDefinition(
        dp_code=definition.dp_code,
        range=parsed["range"],
    )


def parse_dp_integer_definition(
    definition: TuyaDataPointDefinition,
    *,
    target_type: type[TuyaIntegerTypeDefinition] = TuyaIntegerTypeDefinition,
) -> TuyaIntegerTypeDefinition | None:
    if definition.dp_type != TuyaDPType.INTEGER:
        _LOGGER.warning(
            f"Failed to parse integer definition: expected dp type INTEGER, got {definition.dp_type}"
        )
        return None
    if TYPE_CHECKING:
        assert isinstance(definition.specs.values, str)

    parsed = json.loads(definition.specs.values)
    return target_type(
        dp_code=definition.dp_code,
        min=parsed["min"],
        max=parsed["max"],
        scale=parsed["scale"],
        step=parsed["step"],
        unit=parsed.get("unit"),
        type=parsed.get("type"),
    )


def get_dp_integer_definition(
    device: CustomerDevice,
    dp_code: str | None,
    *,
    prefer_function: bool = False,
    target_type: type[TuyaIntegerTypeDefinition] = TuyaIntegerTypeDefinition,
) -> TuyaIntegerTypeDefinition | None:
    if not (
        definition := get_dp_definition(
            device=device, dp_code=dp_code, prefer_function=prefer_function
        )
    ):
        return None

    return parse_dp_integer_definition(definition, target_type=target_type)
