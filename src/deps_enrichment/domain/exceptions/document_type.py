from .base import BusinessException, NotFoundError

__all__ = ["DocumentTypeNotFound", "ExtraFieldNotFound", "MaxExtraFieldsNumberExceeded"]


class DocumentTypeNotFound(NotFoundError):
    code = "document_type_not_found_error"

    def __init__(self, id_: str) -> None:
        super().__init__(f"Document type `{id_}` not found")


class ExtraFieldNotFound(NotFoundError):
    code = "extra_field_not_found_error"


class MaxExtraFieldsNumberExceeded(BusinessException):
    code = "max_extra_field_number_exceeded_error"
