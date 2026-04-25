from random import randint

from deps_enrichment.api import GetExtraFieldsResponse, SerializedExtraField


def test_from_fields__ok(extra_field_factory):
    fields_size = randint(2, 10)
    extra_fields = extra_field_factory.build_batch(size=fields_size)

    response = GetExtraFieldsResponse.from_fields(extra_fields)

    assert len(response.fields) == fields_size
    for field in response.fields:
        assert isinstance(field, SerializedExtraField)

    raw_response = response.dict(by_alias=True)

    assert len(raw_response["fields"]) == fields_size
    for field in raw_response["fields"]:
        assert isinstance(field, dict)
