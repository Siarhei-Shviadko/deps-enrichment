from typing import Optional

from deps_enrichment.domain.model import ExtraData

from .base import ConfiguredBaseModel

__all__ = ["SerializedExtraData", "SerializedExtraDataResponse"]


class SerializedExtraData(ConfiguredBaseModel):
    name: str
    value: str
    code: Optional[str] = None

    @classmethod
    def from_model(cls, data_field: ExtraData) -> "SerializedExtraData":
        return cls(
            name=data_field.name,
            value=data_field.value,
            code=data_field.code.value,
        )


class SerializedExtraDataResponse(SerializedExtraData):
    type: str

    @classmethod
    def from_model(cls, data_field: ExtraData) -> "SerializedExtraDataResponse":
        return cls(
            code=data_field.code.value,
            name=data_field.name,
            type=data_field.type,
            value=data_field.value,
        )
