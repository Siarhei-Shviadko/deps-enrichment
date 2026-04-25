import pytest

from deps_enrichment.domain.model import (
    Code,
    DocumentType,
    EntityId,
    ExtraField,
    FieldType,
    TenantId,
)


@pytest.fixture
def supplement_repository(repositories):
    yield repositories.supplement()


@pytest.fixture
def document_type_repository(repositories):
    return repositories.document_type()


@pytest.fixture
def document_type_id():
    return EntityId()


@pytest.fixture
def tenant_id(tenant):
    return TenantId(tenant)


@pytest.fixture
def document_type(document_type_id, tenant_id):
    return DocumentType(
        id_=document_type_id,
        tenant_id=tenant_id,
    )


@pytest.fixture
def extra_field(faker):
    return ExtraField(
        code=Code(),
        name=faker.name(),
        type_=FieldType.STRING,
        auto_filled=False,
        display_order=0,
    )


@pytest.fixture
def document_type_with_ef(document_type_id, tenant_id, extra_field):
    return DocumentType(id_=document_type_id, tenant_id=tenant_id, extra_fields=[extra_field])
