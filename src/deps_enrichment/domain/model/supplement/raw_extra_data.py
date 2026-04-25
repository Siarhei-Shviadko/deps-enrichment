from typing import Optional, TypedDict

__all__ = ["RawExtraData"]


class RawExtraData(TypedDict, total=False):
    name: str
    value: str
    code: Optional[str]
