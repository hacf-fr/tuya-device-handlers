"""Test fixtures"""

from unittest.mock import Mock

import pytest
from tuya_sharing import (  # type: ignore[import-untyped]
    CustomerDevice,
    DeviceFunction,
    DeviceStatusRange,
)


@pytest.fixture(name="mock_device")
def device_fixture() -> CustomerDevice:
    """Fixture for a customer device."""
    mock_device = Mock(spec=CustomerDevice)
    mock_device.id = "device_id"
    mock_device.product_id = "product_id"

    mock_device.status = {
        "demo_bitmap": 3,
        "demo_boolean": True,
        "demo_enum": "customize_scene",
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
            values='{"unit": "%","min": 0,"max": 1000,"scale": 1,"step": 1}',
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
            values='{"unit": "%","min": 0,"max": 1000,"scale": 1,"step": 1}',
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
