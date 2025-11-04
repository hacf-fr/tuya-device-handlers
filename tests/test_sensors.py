"""Test utils"""

import dataclasses
from typing import Any

import pytest
from syrupy.assertion import SnapshotAssertion
from tuya_sharing import CustomerDevice  # type: ignore[import-untyped]

from tuya_device_handlers.builder import TuyaSensorDefinition
from tuya_device_handlers.helpers import (
    TuyaDPType,
    get_dp_definition,
    parse_dp_integer_definition,
)
from tuya_device_handlers.registry import QuirksRegistry

from . import create_device
from .const import DEVICE_FIXTURES


def _get_entity_details(
    definition: TuyaSensorDefinition, device: CustomerDevice
) -> dict[str, Any]:
    """Generate snapshot details."""
    entity_details: dict[str, Any] = {
        "native_unit_of_measurement": None,
        "state": (status := device.status.get(definition.key)),
    }

    if dp_definition := get_dp_definition(device, definition.key):
        if dp_definition.dp_type == TuyaDPType.INTEGER:
            int_definition = parse_dp_integer_definition(dp_definition)
            assert int_definition is not None
            entity_details["native_unit_of_measurement"] = int_definition.unit
            if status is not None:
                entity_details["state"] = int_definition.scale_value(status)

    return entity_details


@pytest.mark.parametrize("fixture_filename", DEVICE_FIXTURES)
def test_entities(
    fixture_filename: str,
    filled_quirks_registry: QuirksRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test entities."""
    device = create_device(fixture_filename)

    quirk = filled_quirks_registry.get_quirk_for_device(device)
    assert quirk is not None
    for definition in quirk.sensor_definitions:
        assert dataclasses.asdict(definition) == snapshot(
            name=f"{definition.key}-definition"
        )
        assert _get_entity_details(definition, device) == snapshot(
            name=f"{definition.key}-state"
        )
