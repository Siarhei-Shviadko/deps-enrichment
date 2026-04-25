from sqlalchemy import Column, String, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from deps_enrichment.extras.datasource import metadata

__all__ = ["document_type_table"]

document_type_table = Table(
    "document_type",
    metadata,
    Column("id", String, primary_key=True),
    Column("tenant_id", String, nullable=False),
    Column("extra_fields", JSONB, nullable=True),
    UniqueConstraint("id", "tenant_id", name="unique_document_type_id_tenant_id"),
)
