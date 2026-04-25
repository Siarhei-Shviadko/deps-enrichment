from ..shared import EntityId, TenantId
from .extra_data_factory import ExtraDataFactory
from .raw_extra_data import RawExtraData
from .supplement import Supplement

__all__ = ["SupplementFactory"]


class SupplementFactory:
    @classmethod
    def create(cls, id_: str, tenant_id: str, extra_data: list[RawExtraData]) -> Supplement:
        data = [
            ExtraDataFactory.create(
                name=extra_data_field["name"],
                value=extra_data_field["value"],
                code=extra_data_field["code"],
            )
            for extra_data_field in extra_data
        ]

        return Supplement(id_=EntityId(id_), tenant_id=TenantId(tenant_id), data=data)
