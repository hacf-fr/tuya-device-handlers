"""Test DeviceWrapper classes"""

from typing import Any

import pytest
from syrupy.assertion import SnapshotAssertion
from tuya_sharing import CustomerDevice  # type: ignore[import-untyped]

from tuya_device_handlers.device_wrapper import DeviceWrapper
from tuya_device_handlers.device_wrapper.common import (
    DPCodeTypeInformationWrapper,
)
from tuya_device_handlers.device_wrapper.sensor import (
    ElectricityCurrentJsonWrapper,
    ElectricityCurrentRawWrapper,
    ElectricityPowerJsonWrapper,
    ElectricityPowerRawWrapper,
    ElectricityVoltageJsonWrapper,
    ElectricityVoltageRawWrapper,
    WindDirectionEnumWrapper,
)


def _snapshot_sensor(
    wrapper: DeviceWrapper[Any],
    mock_device: CustomerDevice,
    snapshot: SnapshotAssertion,
) -> None:
    """Snapshot device wrapper."""
    expected = {
        "native_unit": wrapper.native_unit,
        "state": wrapper.read_device_status(mock_device),
        "suggested_unit": wrapper.suggested_unit,
    }
    for key in ("options",):
        if hasattr(wrapper, key):
            expected[key] = getattr(wrapper, key)
    assert expected == snapshot


@pytest.mark.parametrize(
    ("wrapper_type", "dpcode", "status_range", "status"),
    [
        (
            WindDirectionEnumWrapper,
            "demo_enum",
            (
                '{"range": ["north", "north_north_east", "north_east",'
                '"east_north_east","east","east_south_east","south_east",'
                '"south_south_east","south", "south_south_west", "south_west", '
                '"west_south_west", "west", "west_north_west", "north_west", '
                '"north_north_west"]}'
            ),
            "north_north_east",
        ),
        (
            ElectricityCurrentJsonWrapper,
            "demo_json",
            "{}",
            '{"electricCurrent": 599.552, "power": 6.912, "voltage": 52.7}',
        ),
        (
            ElectricityPowerJsonWrapper,
            "demo_json",
            "{}",
            '{"electricCurrent": 599.552, "power": 6.912, "voltage": 52.7}',
        ),
        (
            ElectricityVoltageJsonWrapper,
            "demo_json",
            "{}",
            '{"electricCurrent": 599.552, "power": 6.912, "voltage": 52.7}',
        ),
        (
            ElectricityCurrentRawWrapper,
            "demo_raw",
            "{}",
            "Ag8JJQAASAAACAAAAAAACGME",
        ),
        (
            ElectricityPowerRawWrapper,
            "demo_raw",
            "{}",
            "Ag8JJQAASAAACAAAAAAACGME",
        ),
        (
            ElectricityVoltageRawWrapper,
            "demo_raw",
            "{}",
            "Ag8JJQAASAAACAAAAAAACGME",
        ),
    ],
)
def test_sensor_wrapper(
    wrapper_type: type[DPCodeTypeInformationWrapper[Any]],
    dpcode: str,
    status_range: str,
    status: str,
    mock_device: CustomerDevice,
    snapshot: SnapshotAssertion,
) -> None:
    """Test sensor wrappers."""
    mock_device.status[dpcode] = status
    mock_device.status_range[dpcode].values = status_range
    wrapper = wrapper_type.find_dpcode(mock_device, dpcode)

    assert wrapper
    _snapshot_sensor(wrapper, mock_device, snapshot)


@pytest.mark.parametrize(
    ("wrapper_type", "dpcode", "status_range", "status"),
    [
        (
            WindDirectionEnumWrapper,
            "demo_enum",
            (
                '{"range": ["north", "north_north_east", "north_east",'
                '"east_north_east","east","east_south_east","south_east",'
                '"south_south_east","south", "south_south_west", "south_west", '
                '"west_south_west", "west", "west_north_west", "north_west", '
                '"north_north_west"]}'
            ),
            "north_northh_east",
        ),
        (
            ElectricityCurrentJsonWrapper,
            "demo_json",
            "{}",
            "{}",
        ),
        (
            ElectricityPowerJsonWrapper,
            "demo_json",
            "{}",
            "{}",
        ),
        (
            ElectricityVoltageJsonWrapper,
            "demo_json",
            "{}",
            "{}",
        ),
        (
            ElectricityCurrentRawWrapper,
            "demo_raw",
            "{}",
            "",
        ),
        (
            ElectricityPowerRawWrapper,
            "demo_raw",
            "{}",
            "",
        ),
        (
            ElectricityVoltageRawWrapper,
            "demo_raw",
            "{}",
            "",
        ),
    ],
)
def test_sensor_invalid_value(
    wrapper_type: type[DPCodeTypeInformationWrapper[Any]],
    dpcode: str,
    status_range: str,
    status: str,
    mock_device: CustomerDevice,
) -> None:
    """Test sensor wrappers with invalid or None value."""
    mock_device.status[dpcode] = status
    mock_device.status_range[dpcode].values = status_range
    wrapper = wrapper_type.find_dpcode(mock_device, dpcode)

    assert wrapper
    assert wrapper.read_device_status(mock_device) is None

    # All wrappers return None if status is None
    mock_device.status[dpcode] = None
    assert wrapper.read_device_status(mock_device) is None
