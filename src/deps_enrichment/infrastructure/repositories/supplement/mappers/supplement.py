from deps_enrichment.domain.model import EntityId, TenantId
from deps_enrichment.domain.model.supplement import Supplement

from ..types import SupplementDict
from .extra_data import ExtraDataMapper

__all__ = ["SupplementMapper"]


class SupplementMapper:
    @staticmethod
    def to_dict(supplement: Supplement) -> SupplementDict:
        raw_data = [ExtraDataMapper.to_dict(extra_data) for extra_data in supplement.data]

        return {
            "id": supplement.id(),
            "tenant_id": supplement.tenant_id(),
            "data": raw_data,
        }

    @staticmethod
    def from_dict(supplement_dict: SupplementDict) -> Supplement:
        entity_id = EntityId(supplement_dict["id"])
        tenant_id = TenantId(supplement_dict["tenant_id"])
        data = [ExtraDataMapper.from_dict(extra_data) for extra_data in supplement_dict["data"]]

        return Supplement(
            id_=entity_id,
            tenant_id=tenant_id,
            data=data,
        )
