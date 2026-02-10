"""Quirks for Tuya."""

from __future__ import annotations

from tuya_device_handlers import TUYA_QUIRKS_REGISTRY
from tuya_device_handlers.builder import TuyaDeviceQuirk

(
    TuyaDeviceQuirk()
    .applies_to(category="kt", product_id="f3goccgfj6qino4c")
    .add_dpid_boolean(
        dpid=1,
        dpcode="switch",
    )
    .add_dpid_integer(
        dpid=2,
        dpcode="temp_set",
        int_range={"unit": "℃", "min": 160, "max": 880, "scale": 1, "step": 10},
    )
    .add_dpid_integer(
        dpid=3,
        dpcode="temp_current",
        int_range={"unit": "℃", "min": 0, "max": 600, "scale": 1, "step": 1},
    )
    .add_dpid_enum(
        dpid=4,
        dpcode="mode",
        enum_range=["auto", "cold", "wet", "heat", "fan"],
    )
    .add_dpid_enum(
        dpid=5,
        dpcode="fan_speed_enum",
        enum_range=[
            "auto",
            "low",
            "low_mid",
            "mid",
            "mid_high",
            "high",
            "mute",
            "turbo",
        ],
    )
    .add_dpid_boolean(
        dpid=8,
        dpcode="eco",
    )
    .add_dpid_boolean(
        dpid=9,
        dpcode="drying",
    )
    .add_dpid_boolean(
        dpid=12,
        dpcode="heat",
    )
    .add_dpid_boolean(
        dpid=13,
        dpcode="light",
    )
    .add_dpid_integer(
        dpid=22,
        dpcode="countdown_left",
        int_range={
            "unit": "分钟",
            "min": 0,
            "max": 1440,
            "scale": 0,
            "step": 1,
        },
    )
    .add_dpid_enum(
        dpid=105,
        dpcode="temp_unit_convert",
        enum_range=["c", "f"],
    )
    .add_dpid_boolean(
        dpid=109,
        dpcode="sleep",
    )
    .add_dpid_boolean(
        dpid=110,
        dpcode="health",
    )
    .add_dpid_boolean(
        dpid=111,
        dpcode="cleaning",
    )
    .register(TUYA_QUIRKS_REGISTRY)
)
