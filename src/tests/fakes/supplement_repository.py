from typing import Optional

from deps_enrichment.domain.model import ISupplementRepository, Supplement

__all__ = ["FakeSupplementRepository"]

SupplementIdentifier = tuple[str, str]


class FakeSupplementRepository(ISupplementRepository):
    def __init__(self, fake_db: Optional[dict[SupplementIdentifier, Supplement]] = None) -> None:
        self._supplement_db: Optional[dict[SupplementIdentifier, Supplement]] = {}
        if fake_db:
            self._supplement_db = fake_db

    def supplement_of_id(self, supplement_id: str, tenant_id: str) -> Optional[Supplement]:
        key = self._get_dict_key(supplement_id=supplement_id, tenant_id=tenant_id)
        return self._supplement_db.get(key)

    def save(self, supplement: Supplement) -> None:
        key = self._get_dict_key(supplement_id=supplement.id(), tenant_id=supplement.tenant_id())
        self._supplement_db[key] = supplement

    def delete(self, supplement: Supplement) -> None:
        key = self._get_dict_key(supplement_id=supplement.id(), tenant_id=supplement.tenant_id())
        self._supplement_db.pop(key, None)

    @staticmethod
    def _get_dict_key(*, supplement_id: str, tenant_id: str) -> SupplementIdentifier:
        return supplement_id, tenant_id
