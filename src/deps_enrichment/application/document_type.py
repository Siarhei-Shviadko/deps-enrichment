import logging

from deps_message_flow.commands.producer import CommandProducer

from deps_enrichment.constants import COMMANDS_CHANNEL, COMMANDS_REPLIES_CHANNEL
from deps_enrichment.domain.exceptions import DocumentTypeNotFound
from deps_enrichment.domain.model import (
    DEFAULT_EF_DISPLAY_ORDER,
    DocumentType,
    DocumentTypeFactory,
    ExtraField,
    ExtraFieldData,
    GetDocumentTypes,
    IDocumentTypeRepository,
)

__all__ = ["DocumentTypeService"]


class DocumentTypeService:
    def __init__(
        self,
        command_producer: CommandProducer,
        document_type_repository: IDocumentTypeRepository,
    ):
        self._command_producer = command_producer
        self._document_type_repository = document_type_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def initialize(self) -> None:
        self._command_producer.send(
            COMMANDS_CHANNEL,
            GetDocumentTypes(),
            COMMANDS_REPLIES_CHANNEL,
        )
        self._logger.info("Command GetDocumentTypes sent")

    def save_new_document_types(self, document_types: list[dict[str, str]]) -> None:
        doc_types = [
            DocumentTypeFactory.create(id_=doc_type["document_type_id"], tenant_id=doc_type["tenant_id"])
            for doc_type in document_types
        ]
        self._document_type_repository.save_new_all(doc_types)

    def save_new_document_type(self, document_type_id: str, tenant_id: str) -> None:
        doc_type = DocumentTypeFactory.create(id_=document_type_id, tenant_id=tenant_id)
        self._document_type_repository.save_new(doc_type)

    def delete_document_type(self, document_type_id: str, tenant_id: str) -> None:
        self._document_type_repository.delete(document_type_id, tenant_id)

    def create_extra_field(
        self,
        document_type_id: str,
        tenant_id: str,
        name: str,
        auto_filled: bool,
        display_order: int = DEFAULT_EF_DISPLAY_ORDER,
    ) -> str:
        document_type = self._find_document_type(document_type_id=document_type_id, tenant_id=tenant_id)
        extra_field_code = document_type.add_extra_string_field(
            name=name,
            auto_filled=auto_filled,
            display_order=display_order,
        )
        self._document_type_repository.save(document_type)

        return extra_field_code

    def delete_extra_fields(
        self,
        document_type_id: str,
        tenant_id: str,
        extra_field_codes: list[str],
    ) -> None:
        if (
            document_type := self._document_type_repository.document_type_of_id(document_type_id, tenant_id)
        ) is not None:
            document_type.delete_extra_fields(extra_field_codes)
            self._document_type_repository.save(document_type)

    def get_extra_fields(self, document_type_id: str, tenant_id: str) -> list[ExtraField]:
        document_type = self._find_document_type(document_type_id=document_type_id, tenant_id=tenant_id)

        return document_type.extra_fields

    def update_extra_fields(
        self,
        document_type_id: str,
        tenant_id: str,
        extra_fields_data: list[ExtraFieldData],
    ):
        document_type = self._find_document_type(document_type_id=document_type_id, tenant_id=tenant_id)
        document_type.update_extra_fields(extra_fields_data)
        self._document_type_repository.save(document_type)

    def _find_document_type(self, document_type_id: str, tenant_id: str) -> DocumentType:
        if (document_type := self._document_type_repository.document_type_of_id(document_type_id, tenant_id)) is None:
            raise DocumentTypeNotFound(document_type_id)

        return document_type
