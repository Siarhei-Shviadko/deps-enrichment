import pytest

from deps_enrichment.api.serializers import SaveSupplementRequest, SerializedExtraData


@pytest.fixture
def save_supplement_request(extra_field_factory, extra_field_value) -> SaveSupplementRequest:
    extra_data = []

    for _ in range(2):
        extra_field = extra_field_factory()
        extra_data_field = SerializedExtraData(name=extra_field.name, value=extra_field_value)
        extra_data.append(extra_data_field)

    return SaveSupplementRequest(data=extra_data, document_type_id=None)


@pytest.fixture
def save_supplement_request_with_doc_type(
    extra_field_factory,
    extra_field_value,
    document_type_id,
) -> SaveSupplementRequest:
    extra_data = []

    for _ in range(3):
        extra_field = extra_field_factory()
        extra_data_field = SerializedExtraData(name=extra_field.name, value=extra_field_value, code=extra_field.code())
        extra_data.append(extra_data_field)

    return SaveSupplementRequest(data=extra_data, document_type_id=document_type_id())
