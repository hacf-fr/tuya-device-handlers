"""Test utils"""

from tuya_device_handlers.helpers import TuyaIntegerTypeDefinition


def test_scale_value() -> None:
    """Tset scale_value"""
    definition = TuyaIntegerTypeDefinition(
        "upper_temp", 0, 100, 1, 1, "\u2103", "Integer"
    )
    assert definition.scale_value(10) == 1
    assert definition.scale_value(1) == 0.10
    assert definition.scale_value_back(1) == 10
    assert definition.scale_value_back(10) == 100
