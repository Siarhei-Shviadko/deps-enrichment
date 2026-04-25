from http import HTTPStatus
from random import randint

from starlette.testclient import TestClient

from deps_enrichment.constants import V1_API_PREFIX
from deps_enrichment.domain.exceptions import DocumentTypeNotFound
from deps_enrichment.domain.model import DocumentType, FieldType
from tests.fakes import FakeDocumentTypeRepository

FIRST_ELEMENT = 0


def test_create_extra_field__success(
    client: TestClient,
    fake_document_type_repository: FakeDocumentTypeRepository,
    document_type: DocumentType,
    extra_field_name: str,
):
    fake_document_type_repository.save(document_type=document_type)

    response = client.post(
        f"{V1_API_PREFIX}/document-types/{document_type.id.value}/extra-fields",
        json={"name": extra_field_name},
    )

    assert response.status_code == HTTPStatus.CREATED

    extra_field_code = response.json()["code"]
    assert response.json() == {"code": extra_field_code}

    document_type = fake_document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())
    assert len(document_type.extra_fields) == 1
    assert document_type.extra_fields[FIRST_ELEMENT].name == extra_field_name
    assert document_type.extra_fields[FIRST_ELEMENT].type == FieldType.STRING
    assert document_type.extra_fields[FIRST_ELEMENT].auto_filled is False
    assert document_type.extra_fields[FIRST_ELEMENT].display_order == 0


def test_create_extra_field__doc_type_not_found__error(client, fake_document_type_repository, extra_field_name):
    response = client.post(
        f"{V1_API_PREFIX}/document-types/non_existing_doc_type/extra-fields",
        json={"name": extra_field_name},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_extra_fields__deleted(client, fake_document_type_repository, document_type_with_extra_field):
    fake_document_type_repository.save(document_type=document_type_with_extra_field)

    response = client.delete(
        f"{V1_API_PREFIX}/document-types/{document_type_with_extra_field.id.value}/extra-fields",
        params={"extraFieldCodes": document_type_with_extra_field.extra_fields[0].code()},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

    document_type = fake_document_type_repository.document_type_of_id(
        document_type_with_extra_field.id(), document_type_with_extra_field.tenant_id()
    )
    assert document_type.extra_fields == []


def test_delete_extra_fields__doc_type_not_exist__no_error(client, fake_document_type_repository, document_type):
    response = client.delete(
        f"{V1_API_PREFIX}/document-types/{document_type.id.value}/extra-fields",
        params={"extraFieldCodes": "ef_code"},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_extra_fields__ef_not_exist__no_error(client, fake_document_type_repository, document_type):
    fake_document_type_repository.save(document_type=document_type)

    response = client.delete(
        f"{V1_API_PREFIX}/document-types/{document_type.id.value}/extra-fields",
        params={"extraFieldCodes": "ef_code"},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_extra_fields__auto_filled_ef__error(
    client, fake_document_type_repository, document_type_with_auto_filled_ef
):
    fake_document_type_repository.save(document_type=document_type_with_auto_filled_ef)

    response = client.delete(
        f"{V1_API_PREFIX}/document-types/{document_type_with_auto_filled_ef.id.value}/extra-fields",
        params={"extraFieldCodes": document_type_with_auto_filled_ef.extra_fields[0].code()},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_find_extra_fields__document_type_doesnt_exist__not_found(
    document_type_service_mock,
    document_type_id,
    tenant_id,
    client,
):
    document_type_service_mock.get_extra_fields.side_effect = DocumentTypeNotFound(document_type_id)

    response = client.get(f"{V1_API_PREFIX}/document-types/{document_type_id()}/extra-fields")

    assert response.status_code == HTTPStatus.NOT_FOUND
    document_type_service_mock.get_extra_fields.assert_called_once_with(
        document_type_id=document_type_id(),
        tenant_id=tenant_id(),
    )


def test_find_extra_fields__document_type_exists__fields_dont_exist__empty_list(
    document_type_service_mock,
    document_type_id,
    tenant_id,
    client,
):
    expected_response = {"fields": []}
    document_type_service_mock.get_extra_fields.return_value = []

    response = client.get(f"{V1_API_PREFIX}/document-types/{document_type_id()}/extra-fields")

    assert response.status_code == HTTPStatus.OK
    document_type_service_mock.get_extra_fields.assert_called_once_with(
        document_type_id=document_type_id(),
        tenant_id=tenant_id(),
    )
    json_response = response.json()
    assert json_response == expected_response


def test_find_extra_fields__document_type_exists__fields_exist__ok(
    client,
    document_type_id,
    document_type_service_mock,
    tenant_id,
    extra_field_factory,
):
    fields_size = randint(2, 10)
    extra_fields = extra_field_factory.build_batch(size=fields_size)
    document_type_service_mock.get_extra_fields.return_value = extra_fields

    response = client.get(f"{V1_API_PREFIX}/document-types/{document_type_id()}/extra-fields")

    assert response.status_code == HTTPStatus.OK
    document_type_service_mock.get_extra_fields.assert_called_once_with(
        document_type_id=document_type_id(),
        tenant_id=tenant_id(),
    )
    json_response = response.json()
    assert len(json_response["fields"]) == fields_size


def test_update_extra_fields__updated(
    client: TestClient,
    fake_document_type_repository: FakeDocumentTypeRepository,
    document_type_with_extra_field: DocumentType,
):
    fake_document_type_repository.save(document_type=document_type_with_extra_field)

    response = client.put(
        f"{V1_API_PREFIX}/document-types/{document_type_with_extra_field.id.value}/extra-fields",
        json={
            "extraFields": [
                {
                    "code": document_type_with_extra_field.extra_fields[0].code(),
                    "name": "new name",
                    "order": 1,
                }
            ]
        },
    )

    document_type = fake_document_type_repository.document_type_of_id(
        document_type_with_extra_field.id(), document_type_with_extra_field.tenant_id()
    )

    assert response.status_code == HTTPStatus.OK
    assert len(document_type.extra_fields) == 1
    assert document_type.extra_fields[0].name == "new name"
    assert document_type.extra_fields[0].display_order == 1


def test_update_extra_fields__doc_type_not_exist__error(
    client: TestClient,
    fake_document_type_repository: FakeDocumentTypeRepository,
    document_type: DocumentType,
):
    response = client.put(
        f"{V1_API_PREFIX}/document-types/{document_type.id.value}/extra-fields",
        json={"extraFields": [{"code": "ef_code", "name": "new name"}]},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_extra_fields__ef_not_exist__error(client, fake_document_type_repository, document_type):
    fake_document_type_repository.save(document_type=document_type)

    response = client.put(
        f"{V1_API_PREFIX}/document-types/{document_type.id.value}/extra-fields",
        json={"extraFields": [{"code": "ef_code", "name": "new name"}]},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_extra_fields__update_name__auto_filled_ef__error(
    client: TestClient,
    fake_document_type_repository: FakeDocumentTypeRepository,
    document_type_with_auto_filled_ef: DocumentType,
):
    fake_document_type_repository.save(document_type=document_type_with_auto_filled_ef)

    response = client.put(
        f"{V1_API_PREFIX}/document-types/{document_type_with_auto_filled_ef.id.value}/extra-fields",
        json={"extraFields": [{"code": document_type_with_auto_filled_ef.extra_fields[0].code(), "name": "new name"}]},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_extra_fields__dont_update_name__auto_filled_ef__updated(
    client: TestClient,
    fake_document_type_repository: FakeDocumentTypeRepository,
    document_type_with_auto_filled_ef: DocumentType,
):
    fake_document_type_repository.save(document_type=document_type_with_auto_filled_ef)

    response = client.put(
        f"{V1_API_PREFIX}/document-types/{document_type_with_auto_filled_ef.id.value}/extra-fields",
        json={"extraFields": [{"code": document_type_with_auto_filled_ef.extra_fields[0].code(), "order": 1}]},
    )

    document_type = fake_document_type_repository.document_type_of_id(
        document_type_with_auto_filled_ef.id(), document_type_with_auto_filled_ef.tenant_id()
    )

    assert response.status_code == HTTPStatus.OK
    assert len(document_type.extra_fields) == 1
    assert document_type.extra_fields[0].display_order == 1
