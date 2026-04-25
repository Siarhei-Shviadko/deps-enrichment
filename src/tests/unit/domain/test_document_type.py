import uuid

import pytest

from deps_enrichment.domain.exceptions import (
    AlreadyExistsError,
    ForbiddenError,
    MaxExtraFieldsNumberExceeded,
    NotFoundError,
)
from deps_enrichment.domain.model import DocumentType, FieldType


def test_add_extra_field__ok(document_type: DocumentType, extra_field_name: str):
    document_type.add_extra_string_field(name=extra_field_name, auto_filled=False, display_order=1)

    assert len(document_type.extra_fields) == 1
    assert document_type.extra_fields[0].name == extra_field_name
    assert document_type.extra_fields[0].type == FieldType.STRING
    assert document_type.extra_fields[0].auto_filled is False
    assert document_type.extra_fields[0].display_order == 1


def test_add_extra_field__name_exists__forbidden(document_type_with_extra_field, extra_field_name):
    with pytest.raises(AlreadyExistsError):
        document_type_with_extra_field.add_extra_string_field(name=extra_field_name, auto_filled=False)


def test_add_extra_field__exceeds_max_extra_fields_number__error(document_type):
    for _ in range(DocumentType.MAX_EXTRA_FIELDS):
        document_type.add_extra_string_field(name=uuid.uuid4().hex, auto_filled=False)

    with pytest.raises(MaxExtraFieldsNumberExceeded):
        document_type.add_extra_string_field(name=uuid.uuid4().hex, auto_filled=False)


def test_delete_extra_fields__deleted(document_type_with_extra_field):
    document_type_with_extra_field.delete_extra_fields([document_type_with_extra_field.extra_fields[0].code()])

    assert document_type_with_extra_field.extra_fields == []


def test_delete_extra_fields__not_exist__no_error(document_type):
    document_type.delete_extra_fields(["ef_code"])


def test_delete_extra_fields__auto_filled_ef__forbidden(document_type_with_auto_filled_ef):
    with pytest.raises(ForbiddenError):
        document_type_with_auto_filled_ef.delete_extra_fields(
            [document_type_with_auto_filled_ef.extra_fields[0].code()]
        )


def test_update_extra_fields__updated(document_type_with_extra_field: DocumentType):
    document_type_with_extra_field.update_extra_fields(
        [
            {
                "code": document_type_with_extra_field.extra_fields[0].code(),
                "name": "new name",
                "display_order": 1,
            }
        ]
    )

    assert document_type_with_extra_field.extra_fields[0].name == "new name"
    assert document_type_with_extra_field.extra_fields[0].display_order == 1


def test_update_extra_fields__name_exists__forbidden(document_type_with_two_extra_fields):
    with pytest.raises(AlreadyExistsError):
        document_type_with_two_extra_fields.update_extra_fields(
            [
                {
                    "code": document_type_with_two_extra_fields.extra_fields[1].code(),
                    "name": document_type_with_two_extra_fields.extra_fields[0].name,
                    "display_order": 1,
                }
            ]
        )


def test_update_extra_fields__same_name__no_error(document_type_with_extra_field):
    document_type_with_extra_field.update_extra_fields(
        [
            {
                "code": document_type_with_extra_field.extra_fields[0].code(),
                "name": document_type_with_extra_field.extra_fields[0].name,
                "display_order": 1,
            }
        ]
    )


def test_update_extra_fields__not_exist__raise_error(document_type):
    with pytest.raises(NotFoundError):
        document_type.update_extra_fields(
            [
                {
                    "code": "ef_code",
                    "name": "new name",
                    "display_order": 1,
                }
            ]
        )


def test_update_extra_fields__update_name__auto_filled_ef__forbidden(document_type_with_auto_filled_ef: DocumentType):
    with pytest.raises(ForbiddenError):
        document_type_with_auto_filled_ef.update_extra_fields(
            [
                {
                    "code": document_type_with_auto_filled_ef.extra_fields[0].code(),
                    "name": "new name",
                    "display_order": 1,
                }
            ]
        )


def test_update_extra_fields__dont_update_name__auto_filled_ef__updated(
    document_type_with_auto_filled_ef: DocumentType,
):
    document_type_with_auto_filled_ef.update_extra_fields(
        [
            {
                "code": document_type_with_auto_filled_ef.extra_fields[0].code(),
                "name": document_type_with_auto_filled_ef.extra_fields[0].name,
                "display_order": 1,
            }
        ]
    )

    assert document_type_with_auto_filled_ef.extra_fields[0].display_order == 1
