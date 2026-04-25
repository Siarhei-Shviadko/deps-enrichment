import pytest

from deps_enrichment.application.document_type import DocumentTypeService
from deps_enrichment.domain.exceptions import (
    AlreadyExistsError,
    DocumentTypeNotFound,
    ForbiddenError,
    NotFoundError,
)
from deps_enrichment.domain.model import DocumentType, FieldType
from tests.fakes import FakeDocumentTypeRepository


def test_add_extra_field__ok(
    document_type_service: DocumentTypeService,
    fake_document_type_repository: FakeDocumentTypeRepository,
    document_type: DocumentType,
    extra_field_name: str,
):
    fake_document_type_repository.save(document_type=document_type)
    document_type_service.create_extra_field(
        document_type.id(), document_type.tenant_id(), name=extra_field_name, auto_filled=False, display_order=1
    )
    doc_type = fake_document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert len(doc_type.extra_fields) == 1
    assert doc_type.extra_fields[0].name == extra_field_name
    assert doc_type.extra_fields[0].type == FieldType.STRING
    assert doc_type.extra_fields[0].auto_filled is False
    assert doc_type.extra_fields[0].display_order == 1


def test_add_extra_field__doc_type_not_exist__raise_error(
    document_type_service, fake_document_type_repository, document_type, extra_field_name
):
    with pytest.raises(DocumentTypeNotFound):
        document_type_service.create_extra_field(
            document_type.id(), document_type.tenant_id(), name=extra_field_name, auto_filled=False
        )


def test_add_extra_field__name_exists__raise_error(
    document_type_service, fake_document_type_repository, document_type_with_extra_field, extra_field_name
):
    fake_document_type_repository.save(document_type=document_type_with_extra_field)

    with pytest.raises(AlreadyExistsError):
        document_type_service.create_extra_field(
            document_type_with_extra_field.id(),
            document_type_with_extra_field.tenant_id(),
            name=extra_field_name,
            auto_filled=False,
        )


def test_delete_extra_fields__deleted(
    document_type_service, fake_document_type_repository, document_type_with_extra_field
):
    fake_document_type_repository.save(document_type=document_type_with_extra_field)

    document_type_service.delete_extra_fields(
        document_type_id=document_type_with_extra_field.id(),
        tenant_id=document_type_with_extra_field.tenant_id(),
        extra_field_codes={document_type_with_extra_field.extra_fields[0].code()},
    )

    doc_type = fake_document_type_repository.document_type_of_id(
        document_type_with_extra_field.id(), document_type_with_extra_field.tenant_id()
    )

    assert doc_type.extra_fields == []


def test_delete_extra_fields__doc_type_not_exist__no_error(
    document_type_service, fake_document_type_repository, document_type
):
    document_type_service.delete_extra_fields(
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
        extra_field_codes={"ef_code"},
    )


def test_delete_extra_fields__ef_not_exist__no_error(
    document_type_service, fake_document_type_repository, document_type
):
    fake_document_type_repository.save(document_type=document_type)

    document_type_service.delete_extra_fields(
        document_type_id=document_type.id(),
        tenant_id=document_type.tenant_id(),
        extra_field_codes={"ef_code"},
    )


def test_delete_extra_fields__auto_filled_ef__raise_error(
    document_type_service, fake_document_type_repository, document_type_with_auto_filled_ef
):
    fake_document_type_repository.save(document_type=document_type_with_auto_filled_ef)

    with pytest.raises(ForbiddenError):
        document_type_service.delete_extra_fields(
            document_type_id=document_type_with_auto_filled_ef.id(),
            tenant_id=document_type_with_auto_filled_ef.tenant_id(),
            extra_field_codes={document_type_with_auto_filled_ef.extra_fields[0].code()},
        )


def test_get_extra_fields__document_type_doesnt_exist__not_found(document_type_service, document_type_id, tenant_id):
    with pytest.raises(DocumentTypeNotFound):
        document_type_service.get_extra_fields(document_type_id=document_type_id(), tenant_id=tenant_id())


def test_get_extra_fields__document_type_exists__fields_dont_exist__empty_list(
    fake_document_type_repository,
    document_type_service,
    document_type_id,
    document_type,
    tenant_id,
):
    fake_document_type_repository.save(document_type)
    result = document_type_service.get_extra_fields(document_type_id=document_type_id(), tenant_id=tenant_id())

    assert result == []


def test_get_extra_fields__document_type_exists__fields_exist__ok(
    fake_document_type_repository,
    document_type_with_extra_field,
    document_type_service,
    document_type_id,
    extra_field,
    tenant_id,
):
    fake_document_type_repository.save(document_type_with_extra_field)
    result = document_type_service.get_extra_fields(document_type_id=document_type_id(), tenant_id=tenant_id())

    assert result == [extra_field]


def test_initialize__command_sent(mocker, document_type_service):
    mocked_cp = mocker.patch.object(document_type_service, "_command_producer")
    document_type_service.initialize()
    mocked_cp.send.assert_called_once()


def test_save_new_document_types__saved(
    document_type_id, tenant_id, document_type_service, fake_document_type_repository
):
    document_type_service.save_new_document_types([{"document_type_id": document_type_id(), "tenant_id": tenant_id()}])
    doc_type = fake_document_type_repository.document_type_of_id(document_type_id(), tenant_id())

    assert doc_type.id == document_type_id
    assert doc_type.tenant_id == tenant_id
    assert doc_type.extra_fields == []


def test_save_new_document_types__already_exists__no_changes(
    document_type_with_extra_field, document_type_service, fake_document_type_repository
):
    fake_document_type_repository.save(document_type=document_type_with_extra_field)
    document_type_service.save_new_document_types(
        [
            {
                "document_type_id": document_type_with_extra_field.id(),
                "tenant_id": document_type_with_extra_field.tenant_id(),
            }
        ]
    )
    doc_type = fake_document_type_repository.document_type_of_id(
        document_type_with_extra_field.id(), document_type_with_extra_field.tenant_id()
    )

    assert doc_type.id == document_type_with_extra_field.id
    assert doc_type.tenant_id == document_type_with_extra_field.tenant_id
    assert doc_type.extra_fields == document_type_with_extra_field.extra_fields


def test_save_new_document_type__saved(
    document_type_id, tenant_id, document_type_service, fake_document_type_repository
):
    document_type_service.save_new_document_type(document_type_id(), tenant_id())
    doc_type = fake_document_type_repository.document_type_of_id(document_type_id(), tenant_id())

    assert doc_type.id == document_type_id
    assert doc_type.tenant_id == tenant_id
    assert doc_type.extra_fields == []


def test_save_new_document_type__already_exists__no_changes(
    document_type_with_extra_field, document_type_service, fake_document_type_repository
):
    fake_document_type_repository.save(document_type=document_type_with_extra_field)
    document_type_service.save_new_document_type(
        document_type_with_extra_field.id(), document_type_with_extra_field.tenant_id()
    )
    doc_type = fake_document_type_repository.document_type_of_id(
        document_type_with_extra_field.id(), document_type_with_extra_field.tenant_id()
    )

    assert doc_type.id == document_type_with_extra_field.id
    assert doc_type.tenant_id == document_type_with_extra_field.tenant_id
    assert doc_type.extra_fields == document_type_with_extra_field.extra_fields


def test_delete_document_type__deleted(document_type, document_type_service, fake_document_type_repository):
    fake_document_type_repository.save(document_type=document_type)
    document_type_service.delete_document_type(document_type.id(), document_type.tenant_id())

    assert fake_document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id()) is None


def test_delete_document_type__not_exist__no_error(document_type, document_type_service):
    document_type_service.delete_document_type(document_type.id(), document_type.tenant_id())


def test_update_extra_fields__updated(
    document_type_service: DocumentTypeService,
    fake_document_type_repository: FakeDocumentTypeRepository,
    document_type_with_extra_field: DocumentType,
):
    fake_document_type_repository.save(document_type=document_type_with_extra_field)

    document_type_service.update_extra_fields(
        document_type_id=document_type_with_extra_field.id(),
        tenant_id=document_type_with_extra_field.tenant_id(),
        extra_fields_data=[
            {
                "code": document_type_with_extra_field.extra_fields[0].code(),
                "name": "new name",
                "display_order": 1,
            }
        ],
    )

    doc_type = fake_document_type_repository.document_type_of_id(
        document_type_with_extra_field.id(), document_type_with_extra_field.tenant_id()
    )

    assert len(doc_type.extra_fields) == 1
    assert doc_type.extra_fields[0].name == "new name"
    assert doc_type.extra_fields[0].display_order == 1


def test_update_extra_fields__doc_type_not_exist__raise_error(
    document_type_service, fake_document_type_repository, document_type
):
    with pytest.raises(DocumentTypeNotFound):
        document_type_service.update_extra_fields(
            document_type_id=document_type.id(),
            tenant_id=document_type.tenant_id(),
            extra_fields_data=[{"code": "ef_code", "name": "new name"}],
        )


def test_update_extra_fields__ef_not_exist__raise_error(
    document_type_service, fake_document_type_repository, document_type
):
    fake_document_type_repository.save(document_type=document_type)

    with pytest.raises(NotFoundError):
        document_type_service.update_extra_fields(
            document_type_id=document_type.id(),
            tenant_id=document_type.tenant_id(),
            extra_fields_data=[{"code": "ef_code", "name": "new name", "display_order": 1}],
        )


def test_update_extra_fields__update_name__auto_filled_ef__raise_error(
    document_type_service: DocumentTypeService,
    fake_document_type_repository: FakeDocumentTypeRepository,
    document_type_with_auto_filled_ef: DocumentType,
):
    fake_document_type_repository.save(document_type=document_type_with_auto_filled_ef)

    with pytest.raises(ForbiddenError):
        document_type_service.update_extra_fields(
            document_type_id=document_type_with_auto_filled_ef.id(),
            tenant_id=document_type_with_auto_filled_ef.tenant_id(),
            extra_fields_data=[
                {
                    "code": document_type_with_auto_filled_ef.extra_fields[0].code(),
                    "name": "new name",
                    "display_order": 1,
                }
            ],
        )


def test_update_extra_fields__dont_update_name__auto_filled_ef__updated(
    document_type_service: DocumentTypeService,
    fake_document_type_repository: FakeDocumentTypeRepository,
    document_type_with_auto_filled_ef: DocumentType,
):
    fake_document_type_repository.save(document_type=document_type_with_auto_filled_ef)

    document_type_service.update_extra_fields(
        document_type_id=document_type_with_auto_filled_ef.id(),
        tenant_id=document_type_with_auto_filled_ef.tenant_id(),
        extra_fields_data=[
            {
                "code": document_type_with_auto_filled_ef.extra_fields[0].code(),
                "name": document_type_with_auto_filled_ef.extra_fields[0].name,
                "display_order": 1,
            }
        ],
    )

    doc_type = fake_document_type_repository.document_type_of_id(
        document_type_with_auto_filled_ef.id(), document_type_with_auto_filled_ef.tenant_id()
    )

    assert len(doc_type.extra_fields) == 1
    assert doc_type.extra_fields[0].display_order == 1
