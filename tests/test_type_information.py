"""Test utils"""

import dataclasses
from unittest.mock import Mock

import pytest
from syrupy.assertion import SnapshotAssertion
from tuya_sharing import (  # type: ignore[import-untyped]
    CustomerDevice,
    DeviceFunction,
    DeviceStatusRange,
)

from tuya_device_handlers.type_information import (
    BitmapTypeInformation,
    BooleanTypeInformation,
    EnumTypeInformation,
    IntegerTypeInformation,
    JsonTypeInformation,
    RawTypeInformation,
    StringTypeInformation,
    TypeInformation,
)


@pytest.fixture(name="mock_device")
def device_fixture() -> CustomerDevice:
    """Fixture for a customer device."""
    mock_device = Mock(spec=CustomerDevice)
    mock_device.status = {
        "demo_bitmap": 0,
        "demo_boolean": True,
        "demo_enum": "hot",
        "demo_integer": 123,
        "demo_json": '{"h": 210,"s": 1000,"v": 1000}',
        "demo_raw": "fwceBQF/DgACAX8UAAQB",
        "demo_string": "a_string",
    }
    mock_device.function = {
        "demo_bitmap": DeviceFunction(
            code="demo_bitmap",
            type="Bitmap",
            values='{"label": ["motor_fault"]}',
        ),
        "demo_bitmap_missing_values": DeviceFunction(
            code="demo_bitmap_missing_values",
            type="Bitmap",
            values="{}",
        ),
        "demo_boolean": DeviceFunction(
            code="demo_boolean",
            type="Boolean",
            values="{}",
        ),
        "demo_enum": DeviceFunction(
            code="demo_enum",
            type="Enum",
            values='{"range": ["scene", "customize_scene", "colour"]}',
        ),
        "demo_enum_missing_values": DeviceFunction(
            code="demo_enum_missing_values",
            type="Enum",
            values="{}",
        ),
        "demo_integer": DeviceFunction(
            code="demo_integer",
            type="Integer",
            values='{"unit": "","min": 0,"max": 1000,"scale": 1,"step": 1}',
        ),
        "demo_integer_missing_values": DeviceFunction(
            code="demo_integer_missing_values",
            type="Integer",
            values="{}",
        ),
        "demo_json": DeviceFunction(
            code="demo_json",
            type="Json",
            values="{}",
        ),
        "demo_raw": DeviceFunction(
            code="demo_raw",
            type="Raw",
            values="{}",
        ),
        "demo_string": DeviceFunction(
            code="demo_json",
            type="String",
            values="{}",
        ),
    }
    mock_device.status_range = {
        "demo_bitmap": DeviceFunction(
            code="demo_bitmap",
            type="Bitmap",
            values='{"label": ["motor_fault"]}',
        ),
        "demo_boolean": DeviceStatusRange(
            code="demo_boolean",
            type="Boolean",
            values="{}",
        ),
        "demo_enum": DeviceFunction(
            code="demo_enum",
            type="Enum",
            values='{"range": ["scene", "customize_scene", "colour"]}',
        ),
        "demo_integer": DeviceFunction(
            code="demo_integer",
            type="Integer",
            values='{"unit": "","min": 0,"max": 1000,"scale": 1,"step": 1}',
        ),
        "demo_json": DeviceFunction(
            code="demo_json",
            type="Json",
            values="{}",
        ),
        "demo_raw": DeviceFunction(
            code="demo_raw",
            type="Raw",
            values="{}",
        ),
        "demo_string": DeviceFunction(
            code="demo_json",
            type="String",
            values="{}",
        ),
    }
    return mock_device


@pytest.mark.parametrize(
    ("type_information_type", "dpcode"),
    [
        (BitmapTypeInformation, "demo_bitmap"),
        (BooleanTypeInformation, "demo_boolean"),
        (EnumTypeInformation, "demo_enum"),
        (IntegerTypeInformation, "demo_integer"),
        (JsonTypeInformation, "demo_json"),
        (RawTypeInformation, "demo_raw"),
        (StringTypeInformation, "demo_string"),
        # Invalid (missing type details)
        (BitmapTypeInformation, "demo_bitmap_missing_values"),
        (EnumTypeInformation, "demo_enum_missing_values"),
        (IntegerTypeInformation, "demo_integer_missing_values"),
        # Invalid => return None
        (BitmapTypeInformation, "invalid"),
        (BooleanTypeInformation, "invalid"),
        (EnumTypeInformation, "invalid"),
        (IntegerTypeInformation, "invalid"),
        (JsonTypeInformation, "invalid"),
        (RawTypeInformation, "invalid"),
        (StringTypeInformation, "invalid"),
        (StringTypeInformation, ("some",)),
        (StringTypeInformation, None),
    ],
)
def test_valid_type_information(
    dpcode: str | tuple[str] | None,
    type_information_type: type[TypeInformation],
    snapshot: SnapshotAssertion,
    mock_device: CustomerDevice,
) -> None:
    """Test find_dpcode."""
    type_information = type_information_type.find_dpcode(mock_device, dpcode)

    asdict = (
        None
        if type_information is None
        else dataclasses.asdict(type_information)
    )
    assert asdict == snapshot(name="type_information")


def test_integer_scaling(mock_device: CustomerDevice) -> None:
    """Test scale_value/scale_value_back."""
    type_information = IntegerTypeInformation.find_dpcode(
        mock_device, "demo_integer"
    )

    assert type_information
    assert type_information.scale == 1
    assert type_information.scale_value(150) == 15
    assert type_information.scale_value_back(15) == 150
