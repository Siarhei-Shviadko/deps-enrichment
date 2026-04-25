from deps_enrichment.infrastructure.repositories.supplement.mappers import (
    SupplementMapper,
)


def test_supplement_mapper(supplement_factory):
    supplement = supplement_factory()

    raw_supplement = SupplementMapper.to_dict(supplement)

    assert raw_supplement["id"] == supplement.id()
    assert raw_supplement["tenant_id"] == supplement.tenant_id()

    for raw_extra_data, expected_extra_data in zip(raw_supplement["data"], supplement.data):
        assert raw_extra_data["code"] == expected_extra_data.code()
        assert raw_extra_data["name"] == expected_extra_data.name
        assert raw_extra_data["type"] == expected_extra_data.type.value
        assert raw_extra_data["value"] == expected_extra_data.value

    assert SupplementMapper.from_dict(raw_supplement) == supplement
