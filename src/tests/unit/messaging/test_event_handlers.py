from deps_enrichment.messaging.handlers import (
    document_type_created_handler,
    document_type_deleted_handler,
)


def test_document_type_created_handler__document_type_created(
    document_type_created_message, fake_document_type_repository, document_type_id, tenant_id
):
    document_type_created_handler(document_type_created_message)

    assert fake_document_type_repository.document_type_of_id(document_type_id(), tenant_id())


def test_document_type_deleted_handler__document_type_deleted(
    document_type_deleted_message,
    fake_document_type_repository,
    document_type,
):
    fake_document_type_repository.save(document_type)
    document_type_deleted_handler(document_type_deleted_message)

    assert fake_document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id()) is None
