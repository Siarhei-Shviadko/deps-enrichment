from typing import Any

from deps_enrichment.domain.model import DocumentType, EntityId, TenantId

from .extra_field import ExtraFieldMapper

__all__ = ["DocumentTypeMapper"]


class DocumentTypeMapper:
    @staticmethod
    def from_dict(raw_doc_type: dict[str, Any]) -> DocumentType:
        extra_fields = (
            [ExtraFieldMapper.from_dict(extra_field) for extra_field in raw_doc_type["extra_fields"]]
            if raw_doc_type["extra_fields"] is not None
            else None
        )

        return DocumentType(
            id_=EntityId(raw_doc_type["id"]),
            tenant_id=TenantId(raw_doc_type["tenant_id"]),
            extra_fields=extra_fields,
        )

    @staticmethod
    def to_dict(document_type: DocumentType) -> dict[str, Any]:
        raw_extra_fields = [ExtraFieldMapper.to_dict(extra_field) for extra_field in document_type.extra_fields]
        return {
            "id": document_type.id(),
            "tenant_id": document_type.tenant_id(),
            "extra_fields": raw_extra_fields or None,
        }
