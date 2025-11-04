"""Quirks for Tuya."""

from __future__ import annotations

from tuya_device_handlers import TUYA_QUIRKS_REGISTRY
from tuya_device_handlers.builder import TuyaDeviceQuirk
from tuya_device_handlers.helpers import (
    TuyaCoverDeviceClass,
    TuyaDeviceCategory,
    TuyaDPCode,
    TuyaEntityCategory,
    get_dp_enum_definition,
)

(
    # This model has percent_control / percent_state / situation_set
    # but they never get updated - use control instead to get the state
    TuyaDeviceQuirk()
    .applies_to(category=TuyaDeviceCategory.CL, product_id="lfkr93x0ukp5gaia")
    .add_cover(
        key=TuyaDPCode.CONTROL,
        translation_key="curtain",
        translation_string="[%key:component::cover::entity_component::curtain::name%]",
        device_class=TuyaCoverDeviceClass.CURTAIN,
        set_state_dp_type=lambda device: get_dp_enum_definition(
            device, TuyaDPCode.CONTROL
        ),
        get_state_dp_type=lambda device: get_dp_enum_definition(
            device, TuyaDPCode.CONTROL
        ),
    )
    .add_select(
        key=TuyaDPCode.CONTROL_BACK_MODE,
        translation_key="curtain_motor_mode",
        translation_string="Motor mode",
        entity_category=TuyaEntityCategory.CONFIG,
        state_translations={"forward": "Forward", "back": "Back"},
    )
    .add_sensor(
        key=TuyaDPCode.TIME_TOTAL,
        translation_key="last_operation_duration",
        translation_string="Last operation duration",
        entity_category=TuyaEntityCategory.DIAGNOSTIC,
    )
    .register(TUYA_QUIRKS_REGISTRY)
)
