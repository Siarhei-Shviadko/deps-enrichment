from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response

from deps_enrichment.application import DocumentTypeService
from deps_enrichment.containers import Containers

from ...auth import get_current_user_tenant
from ...marker import MarkerRoute, Visibility
from ...serializers import (
    GetExtraFieldsResponse,
    SaveExtraFieldRequest,
    SaveExtraFieldResponse,
    UpdateExtraFieldsRequest,
)

__all__ = ["extra_field_router"]

extra_field_router = APIRouter(route_class=MarkerRoute, tags=["Extra Field"])


@extra_field_router.post(
    "/document-types/{documentTypeId}/extra-fields",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=HTTPStatus.CREATED,
    response_model=SaveExtraFieldResponse,
)
@inject
def create_extra_field(
    extra_field: SaveExtraFieldRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.document_type_service]),
):
    extra_field_code = application.create_extra_field(
        document_type_id=document_type_id,
        tenant_id=current_tenant,
        name=extra_field.name,
        auto_filled=False,
        display_order=extra_field.display_order,
    )
    return SaveExtraFieldResponse(code=extra_field_code)


@extra_field_router.delete(
    "/document-types/{document_type_id}/extra-fields",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=HTTPStatus.NO_CONTENT,
    response_class=Response,
)
@inject
def delete_extra_fields(
    document_type_id: str,
    extra_field_codes: list[str] = Query(..., alias="extraFieldCodes"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.document_type_service]),
):
    application.delete_extra_fields(
        document_type_id=document_type_id,
        tenant_id=current_tenant,
        extra_field_codes=extra_field_codes,
    )


@extra_field_router.get(
    "/document-types/{documentTypeId}/extra-fields",
    openapi_extra={"visibility": Visibility.INTERNAL},
    response_model=GetExtraFieldsResponse,
)
@inject
def get_extra_fields(
    document_type_id: str = Path(..., alias="documentTypeId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.document_type_service]),
) -> GetExtraFieldsResponse:
    extra_fields = application.get_extra_fields(document_type_id=document_type_id, tenant_id=current_tenant)

    return GetExtraFieldsResponse.from_fields(extra_fields)


@extra_field_router.put(
    "/document-types/{documentTypeId}/extra-fields",
    openapi_extra={"visibility": Visibility.INTERNAL},
    status_code=HTTPStatus.OK,
)
@inject
def update_extra_fields(
    extra_fields: UpdateExtraFieldsRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentTypeService = Depends(Provide[Containers.document_type_service]),
):
    extra_fields_data = [extra_field.dict() for extra_field in extra_fields.extra_fields]
    application.update_extra_fields(
        document_type_id=document_type_id,
        tenant_id=current_tenant,
        extra_fields_data=extra_fields_data,
    )
