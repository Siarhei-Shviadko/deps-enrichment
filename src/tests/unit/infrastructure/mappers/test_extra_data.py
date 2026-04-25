from deps_enrichment.infrastructure.repositories.supplement.mappers import (
    ExtraDataMapper,
)


def test_extra_data_mapper(extra_data_factory):
    extra_data = extra_data_factory()

    raw_extra_data = ExtraDataMapper.to_dict(extra_data)

    assert raw_extra_data["code"] == extra_data.code()
    assert raw_extra_data["name"] == extra_data.name
    assert raw_extra_data["type"] == extra_data.type.value
    assert raw_extra_data["value"] == extra_data.value

    assert ExtraDataMapper.from_dict(raw_extra_data) == extra_data
