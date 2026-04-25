from typing import Optional

from ...exceptions import ExtraDataFieldNamesNotUnique
from ..shared import EntityId, Guard, ImmutableCheck, TenantId
from .extra_data import ExtraData

__all__ = ["Supplement"]


class Supplement:
    id = Guard[EntityId](EntityId, ImmutableCheck())
    tenant_id = Guard[TenantId](TenantId, ImmutableCheck())
    data = Guard[list[ExtraData]](list)

    def __init__(self, id_: EntityId, tenant_id: TenantId, data: Optional[list[ExtraData]] = None):
        self.id = id_
        self.tenant_id = tenant_id
        self.data = data if data is not None else []

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    def check_data_field_name_uniqueness(self) -> None:
        all_field_names = [field.name for field in self.data]
        unique_field_names = set(all_field_names)

        if len(all_field_names) > len(unique_field_names):
            raise ExtraDataFieldNamesNotUnique()
