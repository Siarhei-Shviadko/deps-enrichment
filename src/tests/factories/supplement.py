import factory

from deps_enrichment.domain.model import Supplement

from .extra_data import ExtraDataFactory
from .shared import EntityIdFactory, TenantIdFactory

__all__ = ["SupplementFactory"]


class SupplementFactory(factory.Factory):
    class Meta:
        model = Supplement

    id_ = factory.SubFactory(EntityIdFactory)
    tenant_id = factory.SubFactory(TenantIdFactory)
    data = factory.LazyFunction(lambda: [ExtraDataFactory() for _ in range(5)])
