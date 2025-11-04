"""Test utils"""

import pytest

from tuya_device_handlers import TUYA_QUIRKS_REGISTRY
from tuya_device_handlers.devices import register_tuya_quirks
from tuya_device_handlers.registry import QuirksRegistry


@pytest.fixture(scope="module")
def filled_quirks_registry() -> QuirksRegistry:
    """Mock an old config entry that can be migrated."""
    register_tuya_quirks()
    return TUYA_QUIRKS_REGISTRY
