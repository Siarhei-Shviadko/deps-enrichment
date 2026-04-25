import factory

from deps_enrichment.domain.model import Code, EntityId, TenantId

__all__ = ["EntityIdFactory", "CodeFactory", "TenantIdFactory"]


class EntityIdFactory(factory.Factory):
    class Meta:
        model = EntityId

    value = factory.Faker("uuid4")


class CodeFactory(factory.Factory):
    class Meta:
        model = Code

    value = factory.Faker("word")


class TenantIdFactory(factory.Factory):
    class Meta:
        model = TenantId

    value = factory.Faker("uuid4")
