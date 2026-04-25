import logging

from deps_message_flow.commands.consumer import (
    CommandDispatcher,
    CommandHandlersBuilder,
)
from deps_message_flow.events.subscriber import (
    DomainEventDispatcher,
    DomainEventHandlersBuilder,
)
from deps_message_flow.messaging.consumer import IMessageConsumer
from deps_message_flow.messaging.producer import IMessageProducer

from deps_enrichment.constants import (
    COMMANDS_QUEUE,
    COMMANDS_REPLIES_CHANNEL,
    DOCUMENT_TYPE_EXCHANGER,
    DOCUMENTS_EXCHANGER,
    EVENTS_QUEUE,
)
from deps_enrichment.domain.model import (
    DocumentDeleted,
    DocumentTypeCreated,
    DocumentTypeDeleted,
    GetDocumentTypesReply,
)

_logger = logging.getLogger(__name__)


def make_message_dispatcher(subscriber: IMessageConsumer, producer: IMessageProducer) -> IMessageConsumer:
    from deps_enrichment.messaging.handlers import (  # noqa: WPS433
        document_deleted_handler,
        document_type_created_handler,
        document_type_deleted_handler,
        get_document_types_reply_handler,
    )

    events_handlers = (
        DomainEventHandlersBuilder.for_aggregate_type(DOCUMENT_TYPE_EXCHANGER)
        .on_event(DocumentTypeCreated, document_type_created_handler)
        .on_event(DocumentTypeDeleted, document_type_deleted_handler)
        .and_for_aggregate_type(DOCUMENTS_EXCHANGER)
        .on_event(DocumentDeleted, document_deleted_handler)
        .for_queue(EVENTS_QUEUE)
        .build()
    )

    commands_handlers = (
        CommandHandlersBuilder.from_channel(COMMANDS_REPLIES_CHANNEL)
        .on_message(GetDocumentTypesReply, get_document_types_reply_handler)
        .for_queue(COMMANDS_QUEUE)
        .build()
    )

    ded = DomainEventDispatcher(events_handlers, subscriber)
    ded.initialize()

    cd = CommandDispatcher(commands_handlers, subscriber, producer)
    cd.initialize()

    _logger.info("Start consuming....")

    return subscriber
