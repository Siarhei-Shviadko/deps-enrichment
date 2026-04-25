import logging
from typing import Optional

from deps_enrichment.domain.exceptions import DocumentTypeNotFound, SupplementNotFound
from deps_enrichment.domain.model import (
    IDocumentTypeRepository,
    ISupplementRepository,
    RawExtraData,
    Supplement,
    SupplementFactory,
)

__all__ = ["SupplementService"]


class SupplementService:
    def __init__(
        self,
        supplement_repository: ISupplementRepository,
        document_type_repository: IDocumentTypeRepository,
    ) -> None:
        self._supplement_repository = supplement_repository
        self._document_type_repository = document_type_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def find_supplement(self, supplement_id: str, tenant_id: str) -> Supplement:
        if (supplement := self._supplement_repository.supplement_of_id(supplement_id, tenant_id)) is None:
            raise SupplementNotFound(supplement_id)

        return supplement

    def create_or_modify_supplement(
        self,
        supplement_id: str,
        tenant_id: str,
        extra_data: list[RawExtraData],
        document_type_id: Optional[str] = None,
    ) -> str:
        supplement = SupplementFactory.create(
            id_=supplement_id,
            tenant_id=tenant_id,
            extra_data=extra_data,
        )
        supplement.check_data_field_name_uniqueness()

        if document_type_id is not None:
            if (
                document_type := self._document_type_repository.document_type_of_id(document_type_id, tenant_id)
            ) is None:
                raise DocumentTypeNotFound(document_type_id)

            document_type.ensure_coherence_with(supplement)

        self._supplement_repository.save(supplement)
        return supplement_id

    def delete_supplement(self, supplement_id: str, tenant_id: str) -> None:
        if (supplement := self._supplement_repository.supplement_of_id(supplement_id, tenant_id)) is None:
            return

        self._supplement_repository.delete(supplement)
