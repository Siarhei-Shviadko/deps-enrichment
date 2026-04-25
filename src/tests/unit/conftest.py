import pytest

from deps_enrichment.domain.model import (
    Code,
    DocumentType,
    EntityId,
    ExtraData,
    ExtraField,
    FieldType,
    RawExtraData,
    Supplement,
    TenantId,
)
from tests.fakes import FakeDocumentTypeRepository, FakeSupplementRepository


@pytest.fixture
def postgres_datasource_mock(mocker, containers):
    mock = mocker.Mock(containers.datasources.postgres_datasource())
    containers.datasources.postgres_datasource.override(mock)

    yield mock

    containers.datasources.reset_override()


@pytest.fixture(autouse=True)
def fake_document_type_repository(containers):
    with containers.repositories.document_type.override(FakeDocumentTypeRepository()):
        yield containers.repositories.document_type()


@pytest.fixture
def document_type_service(containers, fake_document_type_repository):
    return containers.document_type_service()


@pytest.fixture
def document_type_service_mock(containers, mocker):
    with containers.document_type_service.override(mocker.Mock(containers.document_type_service.cls)) as service:
        yield service()


@pytest.fixture(autouse=True)
def fake_supplement_repository(containers):
    with containers.reset_singletons(), containers.repositories.supplement.override(FakeSupplementRepository()):
        yield containers.repositories.supplement()


@pytest.fixture
def supplement_service(containers, fake_supplement_repository):
    with containers.reset_singletons():
        yield containers.supplement_service()


@pytest.fixture
def document_type_id():
    return EntityId()


@pytest.fixture
def supplement_id():
    return EntityId()


@pytest.fixture
def tenant_id(tenant):
    return TenantId(tenant)


@pytest.fixture
def code():
    return Code()


@pytest.fixture
def extra_field_name(faker):
    return faker.name()


@pytest.fixture
def extra_data_name(faker):
    return faker.name()


@pytest.fixture
def extra_field_value(faker):
    return faker.word()


@pytest.fixture
def type():
    return FieldType.STRING


@pytest.fixture
def extra_field(code, extra_field_name, type):
    return ExtraField(
        code=code,
        name=extra_field_name,
        type_=type,
        auto_filled=False,
        display_order=0,
    )


@pytest.fixture
def extra_field2(type, faker):
    return ExtraField(
        code=Code(),
        name=faker.name(),
        type_=type,
        auto_filled=False,
        display_order=0,
    )


@pytest.fixture
def extra_field_auto_filled(code, extra_field_name, type):
    return ExtraField(
        code=code,
        name=extra_field_name,
        type_=type,
        auto_filled=True,
        display_order=0,
    )


@pytest.fixture
def document_type(document_type_id, tenant_id):
    return DocumentType(
        id_=document_type_id,
        tenant_id=tenant_id,
    )


@pytest.fixture
def document_type_with_extra_field(document_type_id, tenant_id, extra_field):
    return DocumentType(id_=document_type_id, tenant_id=tenant_id, extra_fields=[extra_field])


@pytest.fixture
def document_type_with_two_extra_fields(document_type_id, tenant_id, extra_field, extra_field2):
    return DocumentType(id_=document_type_id, tenant_id=tenant_id, extra_fields=[extra_field, extra_field2])


@pytest.fixture
def document_type_with_auto_filled_ef(document_type_id, tenant_id, extra_field_auto_filled):
    return DocumentType(
        id_=document_type_id,
        tenant_id=tenant_id,
        extra_fields=[extra_field_auto_filled],
    )


@pytest.fixture
def extra_data(extra_data_factory) -> list[ExtraData]:
    return [extra_data_factory() for _ in range(3)]


@pytest.fixture
def raw_extra_data(extra_data) -> list[RawExtraData]:
    return [
        RawExtraData(name=extra_data_field.name, value=extra_data_field.value, code=extra_data_field.code())
        for extra_data_field in extra_data
    ]


@pytest.fixture
def raw_extra_data_with_doc_type_field(extra_field, extra_field_value) -> list[RawExtraData]:
    return [
        RawExtraData(
            code=extra_field.code.value,
            name=extra_field.name,
            value=extra_field_value,
        )
    ]


@pytest.fixture
def extra_data_with_doc_type_field_and_other_name(extra_field, extra_field_value, extra_data_name) -> list[ExtraData]:
    return [
        ExtraData(
            code=extra_field.code,
            name=extra_data_name,
            type_=extra_field.type,
            value=extra_field_value,
        )
    ]


@pytest.fixture
def supplement(supplement_id, tenant_id, extra_data) -> Supplement:
    return Supplement(id_=supplement_id, tenant_id=tenant_id, data=extra_data)


@pytest.fixture
def supplement_with_doc_type_field(
    supplement_id,
    tenant_id,
    extra_data_with_doc_type_field_and_other_name,
) -> Supplement:
    return Supplement(id_=supplement_id, tenant_id=tenant_id, data=extra_data_with_doc_type_field_and_other_name)
