import logging

from dependency_injector.wiring import Provide, inject
from deps_message_flow.commands.common import CommandReplyOutcome, ReplyMessageHeaders
from deps_message_flow.commands.consumer.command_message import CommandMessage
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_enrichment.api import get_current_user_tenant
from deps_enrichment.application import DocumentTypeService, SupplementService
from deps_enrichment.containers import Containers

logger = logging.getLogger(__name__)

__all__ = ["get_document_types_reply_handler", "document_type_created_handler", "document_type_deleted_handler"]


def is_command_successful(command_message: CommandMessage) -> bool:
    return (
        command_message.message.get_required_header(ReplyMessageHeaders.REPLY_OUTCOME)
        == CommandReplyOutcome.SUCCESS.name
    )


@inject
def get_document_types_reply_handler(  # noqa: WPS463
    command_message: CommandMessage,
    document_type_service: DocumentTypeService = Provide[Containers.document_type_service],
):
    if is_command_successful(command_message):
        document_types = command_message.command.document_types
        document_type_service.save_new_document_types(document_types)
        logger.info("Document types updated successfully")
    else:
        logger.error(f"Failed to get document types. Command headers: {command_message.message.headers}")


@inject
def document_type_created_handler(
    dee: DomainEventEnvelope,
    document_type_service: DocumentTypeService = Provide[Containers.document_type_service],
):
    document_type_service.save_new_document_type(document_type_id=dee.event.document_type, tenant_id=dee.event.tenant)


@inject
def document_type_deleted_handler(
    dee: DomainEventEnvelope,
    document_type_service: DocumentTypeService = Provide[Containers.document_type_service],
):
    document_type_service.delete_document_type(document_type_id=dee.event.document_type, tenant_id=dee.event.tenant)


@inject
def document_deleted_handler(
    dee: DomainEventEnvelope,
    supplement_service: SupplementService = Provide[Containers.supplement_service],
):
    supplement_service.delete_supplement(supplement_id=dee.event.document_id, tenant_id=get_current_user_tenant())
