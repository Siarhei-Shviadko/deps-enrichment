from .base import BusinessException, NotFoundError

__all__ = ["SupplementNotFound", "ExtraDataFieldNamesNotUnique", "InconsistentSupplementData"]


class SupplementNotFound(NotFoundError):
    code = "supplement_not_found_error"

    def __init__(self, supplement_id: str) -> None:
        super().__init__(
            f"Supplement with document id `{supplement_id}` not found",
        )


class ExtraDataFieldNamesNotUnique(BusinessException):
    code = "extra_data_field_names_error"

    def __init__(self) -> None:
        super().__init__("ExtraData field names are not unique")


class InconsistentSupplementData(BusinessException):
    code = "inconsistent_supplement_data_fields_error"

    def __init__(self, inconsistent_fields: dict[str, str]) -> None:
        super().__init__(
            f"Supplement data inconsistent with document type for fields: "
            f"`{[(code, inconsistent_fields[code]) for code in inconsistent_fields.keys()]}`",
        )
