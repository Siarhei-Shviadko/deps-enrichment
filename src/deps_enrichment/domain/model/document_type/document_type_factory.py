from ..shared import EntityId, TenantId
from .document_type import DocumentType

__all__ = ["DocumentTypeFactory"]


class DocumentTypeFactory:
    @classmethod
    def create(cls, id_: str, tenant_id: str) -> DocumentType:
        return DocumentType(
            id_=EntityId(id_),
            tenant_id=TenantId(tenant_id),
        )
