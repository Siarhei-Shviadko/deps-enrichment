from ..shared import Code, FieldType, FormatCheck, Guard, ImmutableCheck

__all__ = ["ExtraData"]


class ExtraData:
    code = Guard[Code](Code)
    name = Guard[str](str, FormatCheck(r"^\S(?:\s?\S)*$"), ImmutableCheck())
    type = Guard[FieldType](FieldType)
    value = Guard[str](str, ImmutableCheck())

    def __init__(self, code: Code, name: str, type_: FieldType, value: str):
        self.code = code
        self.name = name
        self.type = type_
        self.value = value

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)  # noqa: WPS222
            and self.code == other.code
            and self.name == other.name
            and self.type == other.type
            and self.value == other.value
        )

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"<class '{self.__class__.__name__}':",
                f"{self.code =},",
                f"{self.name =},",
                f"{self.type =},",
                f"{self.value =}>",
            ),
        )
