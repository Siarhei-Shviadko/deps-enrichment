from sqlalchemy import Column, String, Table
from sqlalchemy.dialects.postgresql import JSONB

from deps_enrichment.extras.datasource import metadata

__all__ = ["supplement_table"]


supplement_table = Table(
    "supplement",
    metadata,
    Column("id", String, primary_key=True),
    Column("tenant_id", String, nullable=False),
    Column("data", JSONB, nullable=False),
)
