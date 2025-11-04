"""Quirks for Tuya."""

from __future__ import annotations

from tuya_device_handlers import TUYA_QUIRKS_REGISTRY
from tuya_device_handlers.builder import TuyaDeviceQuirk
from tuya_device_handlers.helpers import (
    TuyaClimateHVACMode,
    TuyaDeviceCategory,
    TuyaDPCode,
    TuyaEntityCategory,
    TuyaIntegerTypeDefinition,
    get_dp_integer_definition,
)


class CustomIntegerTypeDefinition(TuyaIntegerTypeDefinition):
    @property
    def step_scaled(self) -> float:
        """Return the step scaled."""
        return self.step / (10**self.scale)

    def scale_value(self, value: int) -> float:
        return value / 2

    def scale_value_back(self, value: float) -> int:
        return round(value * 2)


(
    TuyaDeviceQuirk()
    .applies_to(category=TuyaDeviceCategory.WK, product_id="IAYz2WK1th0cMLmL")
    .add_climate(
        key="wk",
        switch_only_hvac_mode=TuyaClimateHVACMode.HEAT_COOL,
        current_temperature_dp_type=lambda device: get_dp_integer_definition(
            device,
            TuyaDPCode.UPPER_TEMP,
            target_type=CustomIntegerTypeDefinition,
        ),
        target_temperature_dp_type=lambda device: get_dp_integer_definition(
            device,
            TuyaDPCode.TEMP_SET,
            target_type=CustomIntegerTypeDefinition,
        ),
    )
    .add_switch(
        key=TuyaDPCode.CHILD_LOCK,
        translation_key="child_lock",
        translation_string="Child lock",
        entity_category=TuyaEntityCategory.CONFIG,
    )
    .register(TUYA_QUIRKS_REGISTRY)
)
