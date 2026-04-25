from typing import Optional

from ..shared import Code, FieldType
from .extra_data import ExtraData

__all__ = ["ExtraDataFactory"]


class ExtraDataFactory:
    @classmethod
    def create(cls, name: str, value: str, code: Optional[str] = None) -> ExtraData:
        return ExtraData(
            code=Code(code) or Code(),
            name=name,
            type_=FieldType.STRING,
            value=value,
        )
