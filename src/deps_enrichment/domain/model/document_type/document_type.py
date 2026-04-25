from typing import Callable, Optional

from ...exceptions import (
    AlreadyExistsError,
    ExtraFieldNotFound,
    ForbiddenError,
    InconsistentSupplementData,
    MaxExtraFieldsNumberExceeded,
)
from ..shared import Code, EntityId, FieldType, Guard, ImmutableCheck, TenantId
from ..supplement import Supplement
from .constants import DEFAULT_EF_DISPLAY_ORDER
from .extra_field import ExtraField
from .extra_field_data import ExtraFieldData

__all__ = ["DocumentType"]

CoherenceCheck = Callable[[Supplement], dict[str, str]]


class DocumentType:
    MAX_EXTRA_FIELDS = 20

    id = Guard[EntityId](EntityId, ImmutableCheck())
    tenant_id = Guard[TenantId](TenantId, ImmutableCheck())

    def __init__(self, id_: EntityId, tenant_id: TenantId, extra_fields: Optional[list[ExtraField]] = None):
        self.id = id_
        self.tenant_id = tenant_id
        self._extra_fields_storage: dict[str, ExtraField] = (
            {field.code(): field for field in extra_fields} if extra_fields is not None else {}
        )

        self._supplement_coherence_checks: list[CoherenceCheck] = [
            self._check_supplement_coherence_by_code,
            self._check_supplement_coherence_by_name,
        ]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    @property
    def extra_fields(self) -> list[ExtraField]:
        return list(self._extra_fields_storage.values())

    def add_extra_string_field(
        self,
        name: str,
        auto_filled: bool,
        display_order: int = DEFAULT_EF_DISPLAY_ORDER,
    ) -> str:
        self._check_max_ef_number_not_exceeded()
        self._check_ef_name_uniqueness(name)

        extra_field_code = Code()
        extra_field = ExtraField(
            code=extra_field_code,
            name=name,
            type_=FieldType.STRING,
            auto_filled=auto_filled,
            display_order=display_order,
        )
        self._extra_fields_storage[extra_field_code()] = extra_field

        return extra_field_code()

    def update_extra_fields(self, extra_fields_data: list[ExtraFieldData]) -> None:
        for extra_field_data in extra_fields_data:
            self._update_extra_field(
                code=extra_field_data["code"],
                name=extra_field_data["name"],
                display_order=extra_field_data["display_order"],
            )

    def delete_extra_fields(self, codes: list[str]):
        for code in codes:
            if (extra_field := self._extra_fields_storage.get(code)) is not None:
                self._check_ef_modifiable(extra_field)
                del self._extra_fields_storage[code]

    def get_extra_field_by_name(self, name: str) -> Optional[ExtraField]:
        return next((field for field in self.extra_fields if field.name == name), None)

    def ensure_coherence_with(self, supplement: Supplement) -> None:
        inconsistent_fields = {}

        for coherence_check in self._supplement_coherence_checks:
            inconsistent_fields.update(coherence_check(supplement))

        if inconsistent_fields:
            raise InconsistentSupplementData(inconsistent_fields)

    def _check_supplement_coherence_by_code(self, supplement: Supplement) -> dict[str, str]:
        inconsistent_fields = {}

        for data_field in supplement.data:
            if extra_field := self._extra_fields_storage.get(data_field.code()):
                if extra_field.name != data_field.name:
                    inconsistent_fields[data_field.code()] = data_field.name

                if extra_field.type != data_field.type:
                    inconsistent_fields[data_field.code()] = data_field.type

        return inconsistent_fields

    def _check_supplement_coherence_by_name(self, supplement: Supplement) -> dict[str, str]:
        inconsistent_fields = {}

        for data_field in supplement.data:
            if extra_field := self.get_extra_field_by_name(data_field.name):
                if extra_field.code() != data_field.code():
                    inconsistent_fields[data_field.code()] = data_field.name

        return inconsistent_fields

    def _update_extra_field(self, code: str, name: Optional[str], display_order: Optional[int]) -> None:
        extra_field = self._find_extra_field(code)

        if name is not None and name != extra_field.name:
            self._check_ef_name_uniqueness(name)
            self._check_ef_modifiable(extra_field)

        self._extra_fields_storage[code] = extra_field.create_updated(name=name, display_order=display_order)

    @staticmethod
    def _check_ef_modifiable(extra_field: ExtraField) -> None:
        if extra_field.auto_filled is True:
            raise ForbiddenError(f"Can't delete or modify automatically added extra field: {extra_field.code.value}")

    def _check_ef_name_uniqueness(self, name: str) -> None:
        if self.get_extra_field_by_name(name) is not None:
            raise AlreadyExistsError(f"Extra field with name {name} for document type {self.id} already exists")

    def _check_max_ef_number_not_exceeded(self) -> None:
        if len(self._extra_fields_storage) >= self.MAX_EXTRA_FIELDS:
            raise MaxExtraFieldsNumberExceeded(
                f"The number of extra fields per document type can't exceed {self.MAX_EXTRA_FIELDS}",
            )

    def _find_extra_field(self, code: str) -> ExtraField:
        if (extra_field := self._extra_fields_storage.get(code)) is None:
            raise ExtraFieldNotFound(f"Extra field with code {code} does not exist")

        return extra_field
