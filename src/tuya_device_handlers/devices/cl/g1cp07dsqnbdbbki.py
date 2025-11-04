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
    get_dp_integer_definition,
)

(
    # This model has percent_state and percent_control but percent_state never
    # gets updated - force percent_control instead
    TuyaDeviceQuirk()
    .applies_to(category=TuyaDeviceCategory.CL, product_id="g1cp07dsqnbdbbki")
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
        set_position_dp_type=lambda device: get_dp_integer_definition(
            device, TuyaDPCode.PERCENT_CONTROL
        ),
        get_position_dp_type=lambda device: get_dp_integer_definition(
            device, TuyaDPCode.PERCENT_CONTROL
        ),
    )
    .add_select(
        key=TuyaDPCode.CONTROL_BACK_MODE,
        translation_key="curtain_motor_mode",
        translation_string="Motor mode",
        entity_category=TuyaEntityCategory.CONFIG,
        state_translations={"forward": "Forward", "back": "Back"},
    )
    .register(TUYA_QUIRKS_REGISTRY)
)
