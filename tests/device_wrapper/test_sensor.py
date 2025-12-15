"""Test DeviceWrapper classes"""

import pytest
from syrupy.assertion import SnapshotAssertion
from tuya_sharing import CustomerDevice  # type: ignore[import-untyped]

from tuya_device_handlers.device_wrapper import DeviceWrapper
from tuya_device_handlers.device_wrapper.sensor import (
    EnumWindDirectionWrapper,
    JsonElectricityCurrentWrapper,
    JsonElectricityPowerWrapper,
    JsonElectricityVoltageWrapper,
    RawElectricityCurrentWrapper,
    RawElectricityPowerWrapper,
    RawElectricityVoltageWrapper,
)


def _snapshot_sensor(
    wrapper: DeviceWrapper,
    mock_device: CustomerDevice,
    snapshot: SnapshotAssertion,
) -> None:
    """Snapshot device wrapper."""
    assert {
        "options": wrapper.range,
        "native_unit": wrapper.native_unit,
        "state": wrapper.read_device_status(mock_device),
        "suggested_unit": wrapper.suggested_unit,
    } == snapshot


@pytest.mark.parametrize(
    ("wrapper_type", "dpcode", "status_range", "status"),
    [
        (
            EnumWindDirectionWrapper,
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
            JsonElectricityCurrentWrapper,
            "demo_json",
            "{}",
            '{"electricCurrent": 599.552, "power": 6.912, "voltage": 52.7}',
        ),
        (
            JsonElectricityPowerWrapper,
            "demo_json",
            "{}",
            '{"electricCurrent": 599.552, "power": 6.912, "voltage": 52.7}',
        ),
        (
            JsonElectricityVoltageWrapper,
            "demo_json",
            "{}",
            '{"electricCurrent": 599.552, "power": 6.912, "voltage": 52.7}',
        ),
        (
            RawElectricityCurrentWrapper,
            "demo_raw",
            "{}",
            "Ag8JJQAASAAACAAAAAAACGME",
        ),
        (
            RawElectricityPowerWrapper,
            "demo_raw",
            "{}",
            "Ag8JJQAASAAACAAAAAAACGME",
        ),
        (
            RawElectricityVoltageWrapper,
            "demo_raw",
            "{}",
            "Ag8JJQAASAAACAAAAAAACGME",
        ),
    ],
)
def test_sensor_wrapper(
    wrapper_type: type[DeviceWrapper],
    dpcode: str,
    status_range: str,
    status: str,
    mock_device: CustomerDevice,
    snapshot: SnapshotAssertion,
) -> None:
    """Test EnumWindDirectionWrapper."""
    mock_device.status[dpcode] = status
    mock_device.status_range[dpcode].values = status_range
    wrapper = wrapper_type.find_dpcode(mock_device, dpcode)

    assert wrapper
    _snapshot_sensor(wrapper, mock_device, snapshot)


def test_wind_wrapper(mock_device: CustomerDevice) -> None:
    """Test EnumWindDirectionWrapper."""
    dpcode = "demo_enum"
    enum_range = (
        '{"range": ["north", "north_north_east", "north_east",'
        '"east_north_east","east","east_south_east","south_east",'
        '"south_south_east","south", "south_south_west", "south_west", '
        '"west_south_west", "west", "west_north_west", "north_west", '
        '"north_north_west"]}'
    )

    mock_device.status_range[dpcode].values = enum_range
    wrapper = EnumWindDirectionWrapper.find_dpcode(mock_device, dpcode)

    assert wrapper

    # All wrappers return None if status is None
    mock_device.status[dpcode] = None
    assert wrapper.read_device_status(mock_device) is None

    # All wrappers return None if status is missing
    mock_device.status.pop(dpcode)
    assert wrapper.read_device_status(mock_device) is None

    # All wrappers return None if status is missing
    mock_device.status[dpcode] = "north_north_west"
    assert wrapper.read_device_status(mock_device) == 337.5

    # All wrappers return None if status is missing
    mock_device.status[dpcode] = "invalid"
    assert wrapper.read_device_status(mock_device) is None
