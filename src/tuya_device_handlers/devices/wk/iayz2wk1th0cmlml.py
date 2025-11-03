"""Quirks for Tuya."""

from __future__ import annotations

from tuya_device_handlers import TUYA_QUIRKS_REGISTRY
from tuya_device_handlers.builder import TuyaDeviceQuirk
from tuya_device_handlers.helpers import (
    TuyaClimateHVACMode,
    TuyaDeviceCategory,
    TuyaDPCode,
    TuyaEntityCategory,
)


def _read_temperature(_device, _def, value: int) -> float:
    return value / 2


def _write_temperature(_device, _def, value: float) -> int:
    return round(value * 2)


(
    TuyaDeviceQuirk()
    .applies_to(category=TuyaDeviceCategory.WK, product_id="IAYz2WK1th0cMLmL")
    .add_climate(
        key="wk",
        switch_only_hvac_mode=TuyaClimateHVACMode.HEAT_COOL,
        current_temperature_dp_code=TuyaDPCode.UPPER_TEMP,
        # UPPER_TEMP uses incorrect scale 1 / step 5 - convert to proper temperature
        current_temperature_state_conversion=_read_temperature,
        # TEMP_SET uses incorrect scale 0 / step 5 - convert to proper temperature
        target_temperature_dp_code=TuyaDPCode.TEMP_SET,
        target_temperature_state_conversion=_read_temperature,
        target_temperature_command_conversion=_write_temperature,
    )
    .add_switch(
        key=TuyaDPCode.CHILD_LOCK,
        translation_key="child_lock",
        translation_string="Child lock",
        entity_category=TuyaEntityCategory.CONFIG,
    )
    .register(TUYA_QUIRKS_REGISTRY)
)
