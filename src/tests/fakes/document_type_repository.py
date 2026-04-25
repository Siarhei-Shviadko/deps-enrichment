from typing import Optional

from deps_enrichment.domain.model import DocumentType, IDocumentTypeRepository

__all__ = ["FakeDocumentTypeRepository"]

DocTypeIdentifier = tuple[str, str]


class FakeDocumentTypeRepository(IDocumentTypeRepository):
    def __init__(self, fake_db: Optional[dict[DocTypeIdentifier, DocumentType]] = None) -> None:
        self._db = {} if fake_db is None else fake_db

    def document_type_of_id(self, document_type_id: str, tenant_id: str) -> Optional[DocumentType]:
        return self._db.get((document_type_id, tenant_id))

    def save(self, document_type: DocumentType) -> None:
        self._db[(document_type.id(), document_type.tenant_id())] = document_type

    def save_new(self, document_type: DocumentType) -> None:
        if self._db.get((document_type.id(), document_type.tenant_id())) is None:
            self._db[document_type.id(), document_type.tenant_id()] = document_type

    def save_new_all(self, document_types: list[DocumentType]) -> None:
        for doc_type in document_types:
            if self._db.get((doc_type.id(), doc_type.tenant_id())) is None:
                self._db[doc_type.id(), doc_type.tenant_id()] = doc_type

    def delete(self, document_type_id: str, tenant_id: str) -> None:
        self._db.pop((document_type_id, tenant_id), None)
