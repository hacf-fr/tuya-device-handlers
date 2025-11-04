"""Quirks for Tuya."""

from __future__ import annotations

from tuya_device_handlers import TUYA_QUIRKS_REGISTRY
from tuya_device_handlers.builder import TuyaDeviceQuirk
from tuya_device_handlers.helpers import (
    TuyaDeviceCategory,
    TuyaDPCode,
    TuyaSensorDeviceClass,
    TuyaSensorStateClass,
    TuyaSwitchDeviceClass,
)

(
    TuyaDeviceQuirk()
    .applies_to(category=TuyaDeviceCategory.CZ, product_id="4mbgrfotyNzMxDAv")
    .add_sensor(
        key=TuyaDPCode.CUR_CURRENT,
        device_class=TuyaSensorDeviceClass.CURRENT,
        state_class=TuyaSensorStateClass.MEASUREMENT,
    )
    .add_sensor(
        key=TuyaDPCode.CUR_POWER,
        device_class=TuyaSensorDeviceClass.POWER,
        state_class=TuyaSensorStateClass.MEASUREMENT,
    )
    .add_sensor(
        key=TuyaDPCode.CUR_VOLTAGE,
        device_class=TuyaSensorDeviceClass.VOLTAGE,
        state_class=TuyaSensorStateClass.MEASUREMENT,
    )
    .add_switch(
        key=TuyaDPCode.SWITCH,
        device_class=TuyaSwitchDeviceClass.OUTLET,
    )
    .register(TUYA_QUIRKS_REGISTRY)
)
