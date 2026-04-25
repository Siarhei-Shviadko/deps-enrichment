from deps_enrichment.domain.model import ExtraDataFactory, Supplement, SupplementFactory


def test_supplement_factory__ok(supplement_id, tenant_id, raw_extra_data):
    supplement = SupplementFactory.create(id_=supplement_id(), tenant_id=tenant_id(), extra_data=raw_extra_data)

    extra_data = [
        ExtraDataFactory.create(
            name=extra_data_field["name"],
            value=extra_data_field["value"],
        )
        for extra_data_field in raw_extra_data
    ]

    assert isinstance(supplement, Supplement)
    assert supplement.id == supplement_id
    assert supplement.tenant_id == tenant_id

    for supplement_extra_field, extra_data_field in zip(supplement.data, extra_data):
        assert supplement_extra_field.name == extra_data_field.name
        assert supplement_extra_field.value == extra_data_field.value
