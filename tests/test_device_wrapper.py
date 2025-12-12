"""Test DeviceWrapper classes"""

import base64
from typing import Any

import pytest
from tuya_sharing import CustomerDevice  # type: ignore[import-untyped]

from tuya_device_handlers.device_wrapper import (
    DPCodeBitmapWrapper,
    DPCodeBooleanWrapper,
    DPCodeEnumWrapper,
    DPCodeIntegerWrapper,
    DPCodeJsonWrapper,
    DPCodeRawWrapper,
    DPCodeStringWrapper,
    DPCodeTypeInformationWrapper,
)


@pytest.mark.parametrize(
    ("wrapper_type", "dpcode", "expected_device_status"),
    [
        (DPCodeBitmapWrapper, "demo_bitmap", 3),
        (DPCodeBooleanWrapper, "demo_boolean", True),
        (DPCodeEnumWrapper, "demo_enum", "customize_scene"),
        (DPCodeIntegerWrapper, "demo_integer", 12.3),
        (DPCodeJsonWrapper, "demo_json", {"h": 210, "s": 1000, "v": 1000}),
        (
            DPCodeRawWrapper,
            "demo_raw",
            base64.b64decode("fwceBQF/DgACAX8UAAQB"),
        ),
        (DPCodeStringWrapper, "demo_string", "a_string"),
    ],
)
def test_read_device_status(
    dpcode: str,
    wrapper_type: type[DPCodeTypeInformationWrapper],
    expected_device_status: Any,
    mock_device: CustomerDevice,
) -> None:
    """Test read_device_status."""
    wrapper = wrapper_type.find_dpcode(mock_device, dpcode)

    assert wrapper
    assert wrapper.read_device_status(mock_device) == expected_device_status


def test_integer_scaling(mock_device: CustomerDevice) -> None:
    """Test scale_value/scale_value_back."""
    wrapper = DPCodeIntegerWrapper.find_dpcode(mock_device, "demo_integer")

    assert wrapper
    assert wrapper.max == 100
    assert wrapper.min == 0
    assert wrapper.step == 0.1
    assert wrapper.native_unit == "%"
