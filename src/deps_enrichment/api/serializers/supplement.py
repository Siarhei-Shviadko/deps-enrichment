from typing import Optional

from pydantic import Field

from deps_enrichment.domain.model import Supplement

from .base import ConfiguredBaseModel
from .extra_data import SerializedExtraData, SerializedExtraDataResponse

__all__ = ["SaveSupplementRequest", "SaveSupplementResponse", "SerializedSupplementResponse"]


class SaveSupplementRequest(ConfiguredBaseModel):
    data: list[SerializedExtraData]
    document_type_id: Optional[str] = Field(alias="documentTypeId")

    def get_raw_data(self):
        return [extra_data_element.dict(by_alias=False) for extra_data_element in self.data]


class SaveSupplementResponse(ConfiguredBaseModel):
    entity_id: str = Field(alias="entityId")


class SerializedSupplementResponse(ConfiguredBaseModel):
    data: list[SerializedExtraDataResponse]

    @classmethod
    def from_model(cls, supplement: Supplement) -> "SerializedSupplementResponse":
        return cls(
            data=[SerializedExtraDataResponse.from_model(data_field) for data_field in supplement.data],
        )
