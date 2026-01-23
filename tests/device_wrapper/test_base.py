"""Test DeviceWrapper classes"""

from tuya_sharing import CustomerDevice  # type: ignore[import-untyped]

from tuya_device_handlers.device_wrapper.base import DeviceWrapper


def test_skip_update(mock_device: CustomerDevice) -> None:
    """Test skip_update."""
    wrapper = DeviceWrapper[str]()

    assert wrapper
    assert wrapper.skip_update(mock_device, None, None) is True
    assert wrapper.skip_update(mock_device, ["a", "b", "c"], {}) is True
