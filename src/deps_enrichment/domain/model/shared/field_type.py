from enum import Enum

__all__ = ["FieldType"]


class FieldType(str, Enum):
    STRING = "string"
