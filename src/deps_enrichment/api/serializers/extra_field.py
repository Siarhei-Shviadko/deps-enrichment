from typing import Optional

from pydantic import Field

from deps_enrichment.domain.model import DEFAULT_EF_DISPLAY_ORDER, ExtraField, FieldType

from .base import ConfiguredBaseModel

__all__ = [
    "SaveExtraFieldRequest",
    "SaveExtraFieldResponse",
    "SerializedExtraField",
    "GetExtraFieldsResponse",
    "UpdateExtraFieldsRequest",
]


class SaveExtraFieldRequest(ConfiguredBaseModel):
    name: str
    display_order: int = Field(default=DEFAULT_EF_DISPLAY_ORDER, alias="order")


class SaveExtraFieldResponse(ConfiguredBaseModel):
    code: str


class SerializedExtraField(ConfiguredBaseModel):
    code: str
    name: str
    type: FieldType
    auto_filled: bool = Field(..., alias="autoFilled")
    display_order: int = Field(..., alias="order")

    @classmethod
    def from_model(cls, field: ExtraField) -> "SerializedExtraField":
        return cls(
            code=field.code(),
            name=field.name,
            type=field.type,
            auto_filled=field.auto_filled,
            display_order=field.display_order,
        )


class GetExtraFieldsResponse(ConfiguredBaseModel):
    fields: list[SerializedExtraField]

    @classmethod
    def from_fields(cls, extra_fields: list[ExtraField]) -> "GetExtraFieldsResponse":
        return cls(fields=[SerializedExtraField.from_model(field) for field in extra_fields])


class UpdateExtraFieldRequest(ConfiguredBaseModel):
    code: str
    name: Optional[str]
    display_order: Optional[int] = Field(default=None, alias="order")


class UpdateExtraFieldsRequest(ConfiguredBaseModel):
    extra_fields: list[UpdateExtraFieldRequest] = Field(..., alias="extraFields")
