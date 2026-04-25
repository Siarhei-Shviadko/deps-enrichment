from typing import Optional

from ..shared import Code, FieldType, FormatCheck, Guard, ImmutableCheck

__all__ = ["ExtraField"]


class ExtraField:
    code = Guard[Code](Code, ImmutableCheck())
    name = Guard[str](str, ImmutableCheck(), FormatCheck(r"^\S(?:\s?\S)*$"))
    type = Guard[FieldType](FieldType, ImmutableCheck())
    auto_filled = Guard[bool](bool, ImmutableCheck())
    display_order = Guard[int](int, ImmutableCheck())

    def __init__(self, code: Code, name: str, type_: FieldType, auto_filled: bool, display_order: int) -> None:
        self.code = code
        self.name = name
        self.type = type_
        self.auto_filled = auto_filled
        self.display_order = display_order

    def create_updated(self, name: Optional[str], display_order: Optional[int]) -> "ExtraField":
        return ExtraField(
            name=name if name is not None else self.name,
            code=self.code,
            type_=self.type,
            auto_filled=self.auto_filled,
            display_order=display_order if display_order is not None else self.display_order,
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)  # noqa: WPS222
            and self.code == other.code
            and self.name == other.name
            and self.type == other.type
            and self.auto_filled == other.auto_filled
            and self.display_order == other.display_order
        )

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"<class '{self.__class__.__name__}':",
                f"{self.code =},",
                f"{self.name =},",
                f"{self.type =},",
                f"{self.auto_filled =},",
                f"{self.display_order =}>",
            ),
        )
