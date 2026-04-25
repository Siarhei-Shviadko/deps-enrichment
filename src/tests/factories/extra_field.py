import factory
from factory.fuzzy import FuzzyChoice

from deps_enrichment.domain.model import Code, ExtraField, FieldType

__all__ = ["ExtraFieldFactory"]


class ExtraFieldFactory(factory.Factory):
    class Meta:
        model = ExtraField

    code = factory.LazyAttribute(lambda obj: Code())
    name = factory.Faker("pystr")
    type_ = FuzzyChoice(FieldType)
    auto_filled = factory.Faker("boolean")
    display_order = factory.Faker("pyint", min_value=0, max_value=1000)
