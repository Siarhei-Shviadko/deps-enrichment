import random

import factory

from deps_enrichment.domain.model import ExtraData, FieldType

from .shared import CodeFactory

__all__ = ["ExtraDataFactory"]


class ExtraDataFactory(factory.Factory):
    class Meta:
        model = ExtraData

    code = factory.LazyFunction(lambda: CodeFactory())
    name = factory.Faker("word")
    type_ = factory.LazyFunction(lambda: random.choice(list(FieldType)))
    value = factory.Faker("word")
