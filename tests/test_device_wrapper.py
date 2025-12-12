"""Test DeviceWrapper classes"""

import base64
from typing import Any

import pytest
from tuya_sharing import CustomerDevice  # type: ignore[import-untyped]
from typeguard import suppress_type_checks

from tuya_device_handlers.device_wrapper import (
    DPCodeBitmapWrapper,
    DPCodeBooleanWrapper,
    DPCodeEnumWrapper,
    DPCodeIntegerWrapper,
    DPCodeJsonWrapper,
    DPCodeRawWrapper,
    DPCodeStringWrapper,
    DPCodeTypeInformationWrapper,
    SetValueOutOfRangeError,
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
    wrapper_type: type[DPCodeTypeInformationWrapper],  # type: ignore [type-arg]
    expected_device_status: Any,
    mock_device: CustomerDevice,
) -> None:
    """Test read_device_status."""
    wrapper = wrapper_type.find_dpcode(mock_device, dpcode)

    assert wrapper
    assert wrapper.read_device_status(mock_device) == expected_device_status

    # All wrappers return None if status is None
    mock_device.status[dpcode] = None
    assert wrapper.read_device_status(mock_device) is None

    # All wrappers return None if status is missing
    mock_device.status.pop(dpcode)
    assert wrapper.read_device_status(mock_device) is None


@pytest.mark.parametrize(
    ("wrapper_type", "dpcode", "value", "expected"),
    [
        (
            DPCodeBooleanWrapper,
            "demo_boolean",
            False,
            [{"code": "demo_boolean", "value": False}],
        ),
        (
            DPCodeEnumWrapper,
            "demo_enum",
            "colour",
            [{"code": "demo_enum", "value": "colour"}],
        ),
        (
            DPCodeIntegerWrapper,
            "demo_integer",
            11.3,
            [{"code": "demo_integer", "value": 113}],
        ),
    ],
)
def test_get_update_commands(
    dpcode: str,
    wrapper_type: type[DPCodeTypeInformationWrapper],  # type: ignore [type-arg]
    value: Any,
    expected: list[dict[str, Any]],
    mock_device: CustomerDevice,
) -> None:
    """Test read_device_status."""
    wrapper = wrapper_type.find_dpcode(mock_device, dpcode)

    assert wrapper
    assert wrapper.get_update_commands(mock_device, value) == expected


@pytest.mark.parametrize(
    ("wrapper_type", "dpcode", "value", "exception_type"),
    [
        (DPCodeBitmapWrapper, "demo_bitmap", 3, NotImplementedError),
        (DPCodeBooleanWrapper, "demo_boolean", "h", SetValueOutOfRangeError),
        (DPCodeEnumWrapper, "demo_enum", "hot", SetValueOutOfRangeError),
        (DPCodeIntegerWrapper, "demo_integer", 111.3, SetValueOutOfRangeError),
        (DPCodeJsonWrapper, "demo_json", {}, NotImplementedError),
        (DPCodeRawWrapper, "demo_raw", b"t", NotImplementedError),
        (DPCodeStringWrapper, "demo_string", "hi", NotImplementedError),
    ],
)
def test_get_update_commands_value_error(
    dpcode: str,
    wrapper_type: type[DPCodeTypeInformationWrapper],  # type: ignore [type-arg]
    value: Any,
    exception_type: type[Exception],
    mock_device: CustomerDevice,
) -> None:
    """Test get_update_commands (ValueError)."""
    wrapper = wrapper_type.find_dpcode(mock_device, dpcode)

    assert wrapper
    with suppress_type_checks(), pytest.raises(exception_type):
        wrapper.get_update_commands(mock_device, value)


def test_integer_details(mock_device: CustomerDevice) -> None:
    """Test scale_value/scale_value_back."""
    wrapper = DPCodeIntegerWrapper.find_dpcode(mock_device, "demo_integer")

    assert wrapper
    assert wrapper.max == 100
    assert wrapper.min == 0
    assert wrapper.step == 0.1
    assert wrapper.native_unit == "%"
