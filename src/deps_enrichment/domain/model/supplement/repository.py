from typing import Optional, Protocol

from .supplement import Supplement

__all__ = ["ISupplementRepository"]


class ISupplementRepository(Protocol):
    def supplement_of_id(self, supplement_id: str, tenant_id: str) -> Optional[Supplement]:
        ...

    def save(self, supplement: Supplement) -> None:
        ...

    def delete(self, supplement: Supplement) -> None:
        ...
