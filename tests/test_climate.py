"""Test utils"""

import dataclasses
from typing import Any

import pytest
from syrupy.assertion import SnapshotAssertion
from tuya_sharing import CustomerDevice

from tuya_device_handlers.builder import TuyaClimateDefinition
from tuya_device_handlers.registry import QuirksRegistry

from . import create_device
from .const import DEVICE_FIXTURES


def _get_entity_details(
    definition: TuyaClimateDefinition, device: CustomerDevice
) -> dict[str, Any]:
    """Generate snapshot details."""
    entity_details: dict[str, Any] = {
        "target_temp": None,
        "target_temp_dp_code": None,
        "target_temp_min": None,
        "target_temp_max": None,
        "target_temp_step": None,
        "current_temp": None,
        "current_temp_dp_code": None,
    }

    if (
        definition.target_temperature_dp_type
        and (int_definition := definition.target_temperature_dp_type(device))
        is not None
    ):
        entity_details["target_temp_dp_code"] = int_definition.dp_code
        entity_details["target_temp_min"] = int_definition.min_scaled
        entity_details["target_temp_max"] = int_definition.max_scaled
        entity_details["target_temp_step"] = int_definition.step_scaled
        if (status := device.status.get(int_definition.dp_code)) is not None:
            entity_details["target_temp"] = int_definition.scale_value(status)

    if (
        definition.current_temperature_dp_type
        and (int_definition := definition.current_temperature_dp_type(device))
        is not None
    ):
        entity_details["current_temp_dp_code"] = int_definition.dp_code
        if (status := device.status.get(int_definition.dp_code)) is not None:
            entity_details["current_temp"] = int_definition.scale_value(status)

    return entity_details


@pytest.mark.parametrize("fixture_filename", DEVICE_FIXTURES)
def test_entities(
    fixture_filename: str,
    filled_quirks_registry: QuirksRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test entities."""
    device = create_device(fixture_filename)

    quirk = filled_quirks_registry.get_quirk_for_device(device)
    assert quirk is not None
    for definition in quirk.climate_definitions:
        assert dataclasses.asdict(definition) == snapshot(
            name=f"{definition.key}-definition"
        )
        assert _get_entity_details(definition, device) == snapshot(
            name=f"{definition.key}-state"
        )
