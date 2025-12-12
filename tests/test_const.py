"""Test constants"""

import pytest

from tuya_device_handlers.const import DPType


@pytest.mark.parametrize(
    ("current_type", "expected_type"),
    [
        ("Boolean", DPType.BOOLEAN),
        ("bool", DPType.BOOLEAN),
        ("boolbool", None),
    ],
)
def test_dptype_parser(
    current_type: str,
    expected_type: DPType | None,
) -> None:
    """Test find_dpcode with invalid dpcode."""
    assert DPType.try_parse(current_type) is expected_type
