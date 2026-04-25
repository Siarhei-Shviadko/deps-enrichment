import pytest

from deps_enrichment.domain.exceptions import (
    DocumentTypeNotFound,
    ExtraDataFieldNamesNotUnique,
    InconsistentSupplementData,
    SupplementNotFound,
)
from deps_enrichment.domain.model import (
    ExtraDataFactory,
    IDocumentTypeRepository,
    ISupplementRepository,
)


def test_create_or_modify_supplement__no_doc_type__ok(
    supplement_service,
    supplement_factory,
    fake_supplement_repository: ISupplementRepository,
    raw_extra_data,
):
    supplement = supplement_factory()

    supplement_id = supplement_service.create_or_modify_supplement(
        supplement_id=supplement.id(), tenant_id=supplement.tenant_id(), extra_data=raw_extra_data
    )

    assert supplement_id == supplement.id()

    saved_supplement = fake_supplement_repository.supplement_of_id(supplement_id, supplement.tenant_id())
    saved_extra_data = [
        ExtraDataFactory.create(
            name=extra_data_field["name"],
            value=extra_data_field["value"],
            code=extra_data_field["code"],
        )
        for extra_data_field in raw_extra_data
    ]

    assert saved_supplement.id() == supplement_id
    assert saved_supplement.tenant_id() == supplement.tenant_id()

    for supplement_extra_field, saved_extra_field in zip(saved_supplement.data, saved_extra_data):
        assert supplement_extra_field.name == saved_extra_field.name
        assert supplement_extra_field.value == saved_extra_field.value
        assert supplement_extra_field.code == saved_extra_field.code


def test_create_or_modify_supplement__with_doc_type_valid__ok(
    supplement_service,
    supplement_factory,
    fake_supplement_repository: ISupplementRepository,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_id,
    document_type_with_extra_field,
    raw_extra_data_with_doc_type_field,
    tenant_id,
):
    fake_document_type_repository.save(document_type=document_type_with_extra_field)
    supplement = supplement_factory()

    supplement_id = supplement_service.create_or_modify_supplement(
        supplement_id=supplement.id(),
        tenant_id=tenant_id(),
        extra_data=raw_extra_data_with_doc_type_field,
        document_type_id=document_type_id(),
    )

    assert supplement_id == supplement.id()

    saved_supplement = fake_supplement_repository.supplement_of_id(supplement_id, tenant_id())
    saved_extra_data = [
        ExtraDataFactory.create(
            name=extra_data_field["name"],
            value=extra_data_field["value"],
            code=extra_data_field["code"],
        )
        for extra_data_field in raw_extra_data_with_doc_type_field
    ]

    assert saved_supplement.id() == supplement_id
    assert saved_supplement.tenant_id() == tenant_id()

    for supplement_extra_field, saved_extra_field in zip(saved_supplement.data, saved_extra_data):
        assert supplement_extra_field.name == saved_extra_field.name
        assert supplement_extra_field.value == saved_extra_field.value


def test_create_supplement__code_and_type_inconsistent_with_doc_type__raised(
    supplement_service,
    supplement_factory,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_id,
    document_type_with_extra_field,
    raw_extra_data_with_doc_type_field,
    tenant_id,
):
    supplement = supplement_factory()
    fake_document_type_repository.save(document_type=document_type_with_extra_field)

    raw_extra_data_with_doc_type_field[0]["name"] = "not matched name"

    with pytest.raises(InconsistentSupplementData):
        supplement_service.create_or_modify_supplement(
            supplement_id=supplement.id(),
            tenant_id=tenant_id(),
            extra_data=raw_extra_data_with_doc_type_field,
            document_type_id=document_type_id(),
        )


def test_create_supplement__name_duplicate_of_extra_field__raised(
    supplement_service,
    supplement_factory,
    fake_document_type_repository: IDocumentTypeRepository,
    document_type_id,
    document_type_with_extra_field,
    raw_extra_data_with_doc_type_field,
    tenant_id,
):
    supplement = supplement_factory()
    fake_document_type_repository.save(document_type=document_type_with_extra_field)

    raw_extra_data_with_doc_type_field[0]["code"] = "not matched code"

    with pytest.raises(InconsistentSupplementData):
        supplement_service.create_or_modify_supplement(
            supplement_id=supplement.id(),
            tenant_id=tenant_id(),
            extra_data=raw_extra_data_with_doc_type_field,
            document_type_id=document_type_id(),
        )


def test_create_or_modify_supplement__with_doc_type_not_exists__raised(
    supplement_service,
    supplement_factory,
    document_type_id,
    raw_extra_data_with_doc_type_field,
    tenant_id,
):
    supplement = supplement_factory()

    with pytest.raises(DocumentTypeNotFound):
        supplement_service.create_or_modify_supplement(
            supplement_id=supplement.id(),
            tenant_id=tenant_id(),
            extra_data=raw_extra_data_with_doc_type_field,
            document_type_id=document_type_id(),
        )


def test_create_or_modify_supplement__with_not_unique_data_field_names__raised(
    supplement_service,
    supplement_factory,
    raw_extra_data,
    tenant_id,
):
    supplement = supplement_factory()
    raw_extra_data[1]["name"] = raw_extra_data[0]["name"]

    with pytest.raises(ExtraDataFieldNamesNotUnique):
        supplement_service.create_or_modify_supplement(
            supplement_id=supplement.id(),
            tenant_id=tenant_id(),
            extra_data=raw_extra_data,
        )


def test_find_supplement__ok(
    supplement_service,
    supplement_factory,
    fake_supplement_repository: ISupplementRepository,
):
    supplement = supplement_factory()
    fake_supplement_repository.save(supplement)

    supplement_from_service = supplement_service.find_supplement(
        supplement_id=supplement.id(),
        tenant_id=supplement.tenant_id(),
    )

    assert supplement_from_service == supplement


def test_find_supplement_not_found__raised(
    supplement_service,
    supplement_factory,
):
    supplement = supplement_factory()

    with pytest.raises(SupplementNotFound):
        supplement_service.find_supplement(
            supplement_id=supplement.id(),
            tenant_id=supplement.tenant_id(),
        )
