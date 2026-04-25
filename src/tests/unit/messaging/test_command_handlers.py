from deps_message_flow.commands.common import CommandReplyOutcome

from deps_enrichment.messaging.handlers import (
    document_deleted_handler,
    get_document_types_reply_handler,
)


def test_get_document_types_reply_handler__success(
    get_document_types_reply_command_message, fake_document_type_repository, document_type_id, tenant_id
):
    get_document_types_reply_command_message.message.get_required_header.return_value = CommandReplyOutcome.SUCCESS.name
    get_document_types_reply_handler(get_document_types_reply_command_message)
    saved_document_type = fake_document_type_repository.document_type_of_id(document_type_id(), tenant_id())

    assert saved_document_type.id == document_type_id
    assert saved_document_type.tenant_id == tenant_id


def test_get_document_types_reply_handler__error(
    get_document_types_reply_command_message, fake_document_type_repository, document_type_id, tenant_id
):
    get_document_types_reply_command_message.message.get_required_header.return_value = CommandReplyOutcome.FAILURE.name
    get_document_types_reply_handler(get_document_types_reply_command_message)
    saved_document_type = fake_document_type_repository.document_type_of_id(document_type_id(), tenant_id())

    assert saved_document_type is None


def test_document_deleted_handler__success(document_deleted_message, fake_supplement_repository, supplement, tenant_id):
    document_deleted_message.message.get_required_header.return_value = CommandReplyOutcome.SUCCESS.name
    fake_supplement_repository.save(supplement)

    created_supplement = fake_supplement_repository.supplement_of_id(supplement.id.value, tenant_id())
    assert created_supplement is not None

    document_deleted_handler(document_deleted_message)
    remaining_supplement = fake_supplement_repository.supplement_of_id(supplement.id.value, tenant_id())

    assert remaining_supplement is None
