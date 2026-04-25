from fastapi import APIRouter

from deps_enrichment.constants import V1_PREFIX

from .extra_field import extra_field_router
from .supplement import supplement_router

__all__ = ["v1_router"]

v1_router = APIRouter(prefix=V1_PREFIX)
v1_router.include_router(extra_field_router)
v1_router.include_router(supplement_router)
