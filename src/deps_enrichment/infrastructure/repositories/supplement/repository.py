from typing import Optional

from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import insert

from deps_enrichment.domain.model import ISupplementRepository, Supplement
from deps_enrichment.extras.datasource import Database

from ...tables import supplement_table
from .mappers import SupplementMapper

__all__ = ["SupplementRepository"]


class SupplementRepository(ISupplementRepository):
    def __init__(self, database: Database) -> None:
        self._db = database

    def save(self, supplement: Supplement) -> None:
        raw_supplement = SupplementMapper.to_dict(supplement)

        with self._db.connection() as conn:
            insert_supplement_query = (
                insert(supplement_table)
                .values(**raw_supplement)
                .on_conflict_do_update(
                    index_elements=[supplement_table.c.id],
                    set_={
                        "data": raw_supplement["data"],
                    },
                )
            )

            conn.execute(insert_supplement_query)

    def supplement_of_id(self, supplement_id: str, tenant_id: str) -> Optional[Supplement]:
        with self._db.connection() as conn:
            get_query = select([supplement_table]).where(
                and_(
                    supplement_table.c.id == supplement_id,
                    supplement_table.c.tenant_id == tenant_id,
                ),
            )

            row = conn.execute(get_query).fetchone()

            if not row:
                return None

            return SupplementMapper.from_dict(row)

    def delete(self, supplement: Supplement) -> None:
        with self._db.connection() as conn:
            delete_query = delete(supplement_table).where(
                and_(
                    supplement_table.c.id == supplement.id(),
                    supplement_table.c.tenant_id == supplement.tenant_id(),
                ),
            )

            conn.execute(delete_query)
