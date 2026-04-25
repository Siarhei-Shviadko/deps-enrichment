from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, status

from deps_enrichment.application import SupplementService
from deps_enrichment.containers import Containers

from ...auth import get_current_user_tenant
from ...marker import MarkerRoute, Visibility
from ...serializers import (
    SaveSupplementRequest,
    SaveSupplementResponse,
    SerializedSupplementResponse,
)

__all__ = ["supplement_router"]

supplement_router = APIRouter(prefix="/supplements", route_class=MarkerRoute, tags=["Supplement"])


@supplement_router.put(
    "/{entityId}",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=status.HTTP_200_OK,
    response_model=SaveSupplementResponse,
)
@inject
def create_or_modify_supplement(
    supplement: SaveSupplementRequest,
    entity_id: str = Path(..., alias="entityId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: SupplementService = Depends(Provide[Containers.supplement_service]),
):
    supplement_id = application.create_or_modify_supplement(
        supplement_id=entity_id,
        tenant_id=current_tenant,
        extra_data=supplement.get_raw_data(),
        document_type_id=supplement.document_type_id,
    )
    return SaveSupplementResponse(entity_id=supplement_id)


@supplement_router.get(
    "/{entityId}",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=status.HTTP_200_OK,
    response_model=SerializedSupplementResponse,
)
@inject
def find_supplement(
    entity_id: str = Path(..., alias="entityId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: SupplementService = Depends(Provide[Containers.supplement_service]),
) -> SerializedSupplementResponse:
    supplement = application.find_supplement(
        supplement_id=entity_id,
        tenant_id=current_tenant,
    )
    return SerializedSupplementResponse.from_model(supplement)
