from typing import Any

from deps_enrichment.domain.model import Code, ExtraField, FieldType

__all__ = ["ExtraFieldMapper"]


class ExtraFieldMapper:
    @staticmethod
    def from_dict(raw_extra_field: dict[str, Any]) -> ExtraField:
        return ExtraField(
            code=Code(raw_extra_field["code"]),
            name=raw_extra_field["name"],
            type_=FieldType(raw_extra_field["type"]),
            auto_filled=raw_extra_field["auto_filled"],
            display_order=raw_extra_field["display_order"],
        )

    @staticmethod
    def to_dict(extra_field: ExtraField) -> dict[str, Any]:
        return {
            "code": extra_field.code(),
            "name": extra_field.name,
            "type": extra_field.type.value,
            "auto_filled": extra_field.auto_filled,
            "display_order": extra_field.display_order,
        }
