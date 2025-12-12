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
        "demo_integer": DeviceFunction(
            code="demo_integer",
            type="Integer",
            values='{"unit": "","min": 0,"max": 100,"scale": 0,"step": 1}',
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
            values='{"unit": "","min": 0,"max": 100,"scale": 0,"step": 1}',
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
        (BitmapTypeInformation, "invalid"),
        (BooleanTypeInformation, "demo_boolean"),
        (BooleanTypeInformation, "invalid"),
        (EnumTypeInformation, "demo_enum"),
        (EnumTypeInformation, "invalid"),
        (IntegerTypeInformation, "demo_integer"),
        (IntegerTypeInformation, "invalid"),
        (JsonTypeInformation, "demo_json"),
        (JsonTypeInformation, "invalid"),
        (RawTypeInformation, "demo_raw"),
        (RawTypeInformation, "invalid"),
        (StringTypeInformation, "demo_string"),
        (StringTypeInformation, "invalid"),
    ],
)
def test_valid_type_information(
    dpcode: str,
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
