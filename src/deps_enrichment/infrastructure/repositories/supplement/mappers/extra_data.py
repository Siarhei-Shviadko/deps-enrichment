from deps_enrichment.domain.model import Code, ExtraData, FieldType

__all__ = ["ExtraDataMapper"]


class ExtraDataMapper:
    @staticmethod
    def to_dict(extra_data: ExtraData) -> dict[str, str]:
        return {
            "code": extra_data.code(),
            "name": extra_data.name,
            "type": extra_data.type.value,
            "value": extra_data.value,
        }

    @staticmethod
    def from_dict(raw_extra_data: dict[str, str]) -> ExtraData:
        code = Code(raw_extra_data["code"])
        field_type = FieldType(raw_extra_data["type"])

        return ExtraData(
            code=code,
            name=raw_extra_data["name"],
            type_=field_type,
            value=raw_extra_data["value"],
        )
