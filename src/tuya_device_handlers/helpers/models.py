"""Tuya models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .const import TuyaDPType

if TYPE_CHECKING:
    from tuya_sharing import (  # type: ignore[import-untyped]
        DeviceFunction,
        DeviceStatusRange,
    )


@dataclass(kw_only=True)
class TuyaDataPointDefinition:
    """Definition of a data point type."""

    dp_code: str
    dp_type: TuyaDPType | None
    specs: DeviceFunction | DeviceStatusRange


@dataclass(kw_only=True)
class TuyaTypeDefinition:
    """Definition of an integer type data."""

    dp_code: str
    dp_type: TuyaDPType | None


@dataclass(kw_only=True)
class TuyaEnumTypeDefinition(TuyaTypeDefinition):
    """Definition of an integer type data."""

    range: list[str]


@dataclass(kw_only=True)
class TuyaIntegerTypeDefinition(TuyaTypeDefinition):
    """Definition of an integer type data."""

    min: int
    max: int
    scale: int
    step: int
    unit: str | None = None
    type: str | None = None

    @property
    def max_scaled(self) -> float:
        """Return the max scaled."""
        return self.scale_value(self.max)

    @property
    def min_scaled(self) -> float:
        """Return the min scaled."""
        return self.scale_value(self.min)

    @property
    def step_scaled(self) -> float:
        """Return the step scaled."""
        return self.scale_value(self.step)

    def scale_value(self, value: int) -> float:
        """Scale a value."""
        return value / (10**self.scale)  # type: ignore[no-any-return]

    def scale_value_back(self, value: float) -> int:
        """Return raw value for scaled."""
        return int(value * (10**self.scale))
