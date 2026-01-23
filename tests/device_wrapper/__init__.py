"""Test DeviceWrapper classes"""

from typing import Any

from tuya_sharing import CustomerDevice  # type: ignore[import-untyped]

from tuya_device_handlers.device_wrapper.base import DeviceWrapper

from .. import send_device_update


def send_wrapper_update(
    device: CustomerDevice,
    wrapper: DeviceWrapper[Any],
    updated_status_properties: dict[str, Any] | None = None,
    dp_timestamps: dict[str, int] | None = None,
) -> None:
    """Send device update, and trigger skip_update"""
    send_device_update(device, updated_status_properties)
    if updated_status_properties:
        wrapper.skip_update(
            device, list(updated_status_properties), dp_timestamps
        )
