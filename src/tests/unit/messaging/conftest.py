import pytest
from deps_message_flow.commands.consumer import CommandMessage
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_enrichment.domain.model import (
    DocumentDeleted,
    DocumentTypeCreated,
    DocumentTypeDeleted,
    GetDocumentTypesReply,
)


@pytest.fixture
def get_document_types_reply_command_message(mocker, document_type_id, tenant_id):
    cm = mocker.Mock(CommandMessage)
    cm.command = GetDocumentTypesReply(
        document_types=[
            {"document_type_id": document_type_id(), "tenant_id": tenant_id()},
        ]
    )
    return cm


@pytest.fixture
def document_type_created_message(mocker, document_type_id, tenant_id):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event = DocumentTypeCreated(document_type=document_type_id(), tenant=tenant_id())
    return dee


@pytest.fixture
def document_type_deleted_message(mocker, document_type):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event = DocumentTypeDeleted(document_type=document_type.id(), tenant=document_type.tenant_id())
    return dee


@pytest.fixture
def document_deleted_message(mocker, supplement_id):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event = DocumentDeleted(document_id=supplement_id.value)
    return dee
