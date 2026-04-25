from typing import Any

from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.dialects.postgresql.dml import Insert
from sqlalchemy.sql import Delete, Select

from ...tables import document_type_table

__all__ = ["DocumentTypeQueryFactory"]


class DocumentTypeQueryFactory:
    def __init__(self) -> None:
        self._document_type_table = document_type_table

    def select_document_type(self, document_type_id: str, tenant_id: str) -> Select:
        return select([self._document_type_table]).where(
            and_(
                self._document_type_table.c.id == document_type_id,
                self._document_type_table.c.tenant_id == tenant_id,
            ),
        )

    def insert_document_type_without_update(self) -> Insert:
        return insert(self._document_type_table).on_conflict_do_nothing()

    def insert_document_type_with_update(self) -> Insert:
        insert_query = insert(self._document_type_table)
        return insert_query.on_conflict_do_update(
            index_elements=[self._document_type_table.c.id, self._document_type_table.c.tenant_id],
            set_={"extra_fields": insert_query.excluded.extra_fields},
        )

    def insert_document_types_without_update(self, raw_doc_types: list[dict[str, Any]]) -> Insert:
        return insert(self._document_type_table).values(raw_doc_types).on_conflict_do_nothing()

    def delete_document_type(self, document_type_id: str, tenant_id: str) -> Delete:
        return delete(self._document_type_table).where(
            and_(
                self._document_type_table.c.id == document_type_id,
                self._document_type_table.c.tenant_id == tenant_id,
            ),
        )
