"""Tuya device wrapper."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .common import DPCodeEnumWrapper

if TYPE_CHECKING:
    from tuya_sharing import CustomerDevice  # type: ignore[import-untyped]


class EnumWindDirectionWrapper(DPCodeEnumWrapper):
    """Custom DPCode Wrapper for converting enum to wind direction."""

    _WIND_DIRECTIONS = {
        "north": 0.0,
        "north_north_east": 22.5,
        "north_east": 45.0,
        "east_north_east": 67.5,
        "east": 90.0,
        "east_south_east": 112.5,
        "south_east": 135.0,
        "south_south_east": 157.5,
        "south": 180.0,
        "south_south_west": 202.5,
        "south_west": 225.0,
        "west_south_west": 247.5,
        "west": 270.0,
        "west_north_west": 292.5,
        "north_west": 315.0,
        "north_north_west": 337.5,
    }

    def read_device_status(self, device: CustomerDevice) -> float | None:
        """Read the device value for the dpcode."""
        if (status := super().read_device_status(device)) is None:
            return None
        return self._WIND_DIRECTIONS.get(status)
