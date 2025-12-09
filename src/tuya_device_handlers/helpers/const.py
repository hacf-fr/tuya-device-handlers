"""Constants for Tuya device handlers."""

from __future__ import annotations

from enum import StrEnum


class TuyaDPType(StrEnum):
    """Data point types."""

    BITMAP = "Bitmap"
    BOOLEAN = "Boolean"
    ENUM = "Enum"
    INTEGER = "Integer"
    JSON = "Json"
    RAW = "Raw"
    STRING = "String"
