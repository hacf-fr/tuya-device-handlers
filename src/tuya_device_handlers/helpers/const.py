"""Constants for Tuya device handlers."""

from __future__ import annotations

from enum import StrEnum


class TuyaDPType(StrEnum):
    """Data point types."""

    BITMAP = "Bitmap"
    BOOLEAN = "Boolean"
    ENUM = "Enum"
    INTEGER = "Integer"
    JSON = "Json"
    RAW = "Raw"
    STRING = "String"


class TuyaDPCode(StrEnum):
    """Tuya data-point codes."""

    CHILD_LOCK = "child_lock"
    CONTROL = "control"
    CONTROL_BACK_MODE = "control_back_mode"
    CUR_CURRENT = "cur_current"
    CUR_POWER = "cur_power"
    CUR_VOLTAGE = "cur_voltage"
    PERCENT_CONTROL = "percent_control"
    SWITCH = "switch"
    SWITCH_1 = "switch_1"
    TEMP_SET = "temp_set"
    TIME_TOTAL = "time_total"
    UPPER_TEMP = "upper_temp"


class TuyaDeviceCategory(StrEnum):
    """Tuya device categories."""

    CL = "cl"
    """Curtain

    https://developer.tuya.com/en/docs/iot/categorycl?id=Kaiuz1hnpo7df
    """
    CZ = "cz"
    """Socket"""
    WK = "wk"
    """Thermostat

    https://developer.tuya.com/en/docs/iot/f?id=K9gf45ld5l0t9
    """
