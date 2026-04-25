from typing import TypedDict

__all__ = ["ExtraFieldData"]


class ExtraFieldData(TypedDict, total=False):
    code: str
    name: str
    display_order: int
