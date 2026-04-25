from http import HTTPStatus

import pytest

from deps_enrichment.api.serializers import SerializedSupplementResponse
from deps_enrichment.constants import V1_API_PREFIX
from deps_enrichment.domain.model import (
    ExtraDataFactory,
    IDocumentTypeRepository,
    ISupplementRepository,
)


@pytest.mark.supplement
def test_create__new_supplement__ok(
    client,
    save_supplement_request,
    fake_supplement_repository: ISupplementRepository,
    supplement_factory,
    tenant,
):
    supplement_to_create = supplement_factory()

    response = client.put(
        f"{V1_API_PREFIX}/supplements/{supplement_to_create.id()}",
        data=save_supplement_request.json(),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["entityId"] == supplement_to_create.id()

    created_supplement = fake_supplement_repository.supplement_of_id(
        supplement_id=supplement_to_create.id(),
        tenant_id=tenant,
    )

    assert created_supplement == supplement_to_create


@pytest.mark.supplement
def test_modify_exist_supplement__ok(
    client,
    save_supplement_request,
    fake_supplement_repository: ISupplementRepository,
    supplement_factory,
    tenant,
):
    supplement_to_update = supplement_factory()
    fake_supplement_repository.save(supplement_to_update)

    raw_extra_data_new = [
        extra_data_element.dict(by_alias=False) for extra_data_element in save_supplement_request.data
    ]
    extra_data_new = [
        ExtraDataFactory.create(
            name=extra_data_field["name"],
            value=extra_data_field["value"],
        )
        for extra_data_field in raw_extra_data_new
    ]

    response = client.put(
        f"{V1_API_PREFIX}/supplements/{supplement_to_update.id()}",
        data=save_supplement_request.json(),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["entityId"] == supplement_to_update.id()

    updated_supplement = fake_supplement_repository.supplement_of_id(
        supplement_id=supplement_to_update.id(),
        tenant_id=tenant,
    )

    assert updated_supplement.id == supplement_to_update.id
    assert updated_supplement.tenant_id() == tenant

    for new_extra_field, updated_extra_field in zip(extra_data_new, updated_supplement.data):
        assert new_extra_field.name == updated_extra_field.name
        assert new_extra_field.value == updated_extra_field.value


@pytest.mark.supplement
def test_create_supplement__code_and_type_inconsistent_with_doc_type__error(
    client,
    save_supplement_request_with_doc_type,
    fake_document_type_repository: IDocumentTypeRepository,
    supplement_factory,
    document_type_with_extra_field,
    extra_field,
):
    fake_document_type_repository.save(document_type=document_type_with_extra_field)
    save_supplement_request_with_doc_type.data[0].name = "fake name"
    save_supplement_request_with_doc_type.data[0].code = extra_field.code()

    supplement_to_create = supplement_factory()

    response = client.put(
        f"{V1_API_PREFIX}/supplements/{supplement_to_create.id()}",
        data=save_supplement_request_with_doc_type.json(),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.supplement
def test_create__supplement__names_duplicated__error(
    client,
    save_supplement_request,
    supplement_factory,
):
    supplement_to_create = supplement_factory()
    save_supplement_request.data[1].name = save_supplement_request.data[0].name

    response = client.put(
        f"{V1_API_PREFIX}/supplements/{supplement_to_create.id()}",
        data=save_supplement_request.json(),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.supplement
def test_create__supplement__name_empty_string__error(
    client,
    save_supplement_request,
    supplement_factory,
):
    supplement_to_create = supplement_factory()
    save_supplement_request.data[1].name = "     "

    response = client.put(
        f"{V1_API_PREFIX}/supplements/{supplement_to_create.id()}",
        data=save_supplement_request.json(),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.supplement
def test_create__new_supplement__doc_type_not_exists__error(
    client,
    save_supplement_request_with_doc_type,
    supplement_factory,
):
    supplement_to_create = supplement_factory()

    response = client.put(
        f"{V1_API_PREFIX}/supplements/{supplement_to_create.id()}",
        data=save_supplement_request_with_doc_type.json(),
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.supplement
def test_find_supplement__ok(
    client,
    fake_supplement_repository: ISupplementRepository,
    supplement,
):
    fake_supplement_repository.save(supplement)

    response = client.get(f"{V1_API_PREFIX}/supplements/{supplement.id()}")

    assert response.status_code == HTTPStatus.OK

    supplement_response = SerializedSupplementResponse.from_model(supplement).dict(by_alias=False)
    assert response.json() == supplement_response


@pytest.mark.supplement
def test_find_supplement__not_found(client, supplement_factory):
    supplement = supplement_factory()
    response = client.get(f"{V1_API_PREFIX}/supplements/{supplement.id()}")

    assert response.status_code == HTTPStatus.NOT_FOUND
