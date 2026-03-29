"""Quirks for Tuya."""

from __future__ import annotations

from tuya_device_handlers import TUYA_QUIRKS_REGISTRY
from tuya_device_handlers.builder import TuyaDeviceQuirk

(
    TuyaDeviceQuirk()
    .applies_to(category="wk", product_id="sqkxklkleeasfk8w")
    .add_dpid_enum(
        dpid=2,
        dpcode="mode",
        enum_range=["auto"],
    )
    .add_dpid_integer(
        dpid=16,
        dpcode="temp_set",
        int_range={
            "unit": "℃",
            "min": 500,
            "max": 3200,
            "scale": 2,
            "step": 50,
        },
    )
    .add_dpid_integer(
        dpid=17,
        dpcode="temp_set_f",
        int_range={"unit": "℉", "min": 41, "max": 90, "scale": 0, "step": 1},
    )
    .add_dpid_integer(
        dpid=18,
        dpcode="upper_temp_f",
        int_range={"unit": "℉", "min": 70, "max": 104, "scale": 0, "step": 1},
    )
    .add_dpid_integer(
        dpid=19,
        dpcode="upper_temp",
        int_range={"unit": "℃", "min": 20, "max": 40, "scale": 0, "step": 1},
    )
    .add_dpid_integer(
        dpid=20,
        dpcode="lower_temp_f",
        int_range={"unit": "℉", "min": 32, "max": 70, "scale": 0, "step": 1},
    )
    .add_dpid_enum(
        dpid=23,
        dpcode="temp_unit_convert",
        enum_range=["c", "f"],
    )
    .add_dpid_integer(
        dpid=24,
        dpcode="temp_current",
        int_range={
            "unit": "℃",
            "min": -5000,
            "max": 5000,
            "scale": 2,
            "step": 50,
        },
    )
    .add_dpid_integer(
        dpid=26,
        dpcode="lower_temp",
        int_range={"unit": "℃", "min": 0, "max": 20, "scale": 0, "step": 1},
    )
    .add_dpid_integer(
        dpid=27,
        dpcode="temp_correction",
        int_range={"min": -9, "max": 9, "scale": 0, "step": 1},
    )
    .add_dpid_integer(
        dpid=29,
        dpcode="temp_current_f",
        int_range={"unit": "℉", "min": -122, "max": 122, "scale": 0, "step": 1},
    )
    .add_dpid_integer(
        dpid=34,
        dpcode="humidity",
        int_range={"unit": "%", "min": 0, "max": 100, "scale": 0, "step": 1},
    )
    .add_dpid_bitmap(
        dpid=45,
        dpcode="fault",
        label_range=["e1", "e2", "e3"],
    )
    .register(TUYA_QUIRKS_REGISTRY)
)
