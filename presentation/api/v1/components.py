from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from application.services.components.query.component_query_service import ComponentQueryService
from application.dependencies.components.query.component_query_dependencies import get_component_query_service
from presentation.schemas.component_schemas import SchemeResponse
from fastapi import HTTPException

router = APIRouter(tags=["Components"])


@router.get("/schemes", response_model=List[SchemeResponse])
async def get_all_schemes(
    is_active: Optional[bool] = Query(None, description="Filter by active status. Omit for all."),
    service: ComponentQueryService = Depends(get_component_query_service),
):
    return await service.get_all_schemes(is_active)


@router.get("/schemes/{scheme_id}", response_model=SchemeResponse)
async def get_scheme_by_id(
    scheme_id: int,
    service: ComponentQueryService = Depends(get_component_query_service),
):
    scheme = await service.get_scheme_by_id(scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme


@router.get("/component-types")
async def get_component_types(
    scheme_id: Optional[int] = Query(None, description="Filter by scheme"),
    is_active: Optional[bool] = Query(True),
    service: ComponentQueryService = Depends(get_component_query_service),
):
    return await service.get_component_types(scheme_id, is_active)


@router.get("/components")
async def get_components(
    scheme_id: Optional[int] = Query(None),
    component_type_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(True),
    service: ComponentQueryService = Depends(get_component_query_service),
):
    return await service.get_components(scheme_id, component_type_id, is_active)


@router.get("/sub-components")
async def get_sub_components(
    scheme_id: Optional[int] = Query(None),
    component_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(True),
    service: ComponentQueryService = Depends(get_component_query_service),
):
    return await service.get_sub_components(scheme_id, component_id, is_active)


@router.get("/crop-items")
async def get_crop_items(
    scheme_id: Optional[int] = Query(None),
    sub_component_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(True),
    service: ComponentQueryService = Depends(get_component_query_service),
):
    return await service.get_crop_items(scheme_id, sub_component_id, is_active)


@router.get("/years")
async def get_years(
    service: ComponentQueryService = Depends(get_component_query_service),
):
    return await service.get_years()


@router.get("/scheme-hierarchy")
async def get_scheme_hierarchy(
    scheme_id: int = Query(...),
    year_code: int = Query(...),
    subsidy_status: Optional[str] = Query(None, description="'assigned' | 'workflow_active' | 'inactive'"),
    service: ComponentQueryService = Depends(get_component_query_service),
):
    return await service.get_scheme_hierarchy(scheme_id, year_code, subsidy_status)


@router.get("/cascade/{scheme_id}")
async def get_cascade_by_scheme(
    scheme_id: int,
    year_code: Optional[int] = Query(None, description="Financial year code e.g. 25 for 2025-26. Defaults to current year."),
    service: ComponentQueryService = Depends(get_component_query_service),
):
    return await service.get_cascade_by_scheme(scheme_id, year_code)


@router.get("/subsidy-assignments")
async def get_subsidy_assignments(
    year_code: int = Query(...),
    scheme_id: Optional[int] = Query(None),
    subsidy_status: Optional[str] = Query(None),
    service: ComponentQueryService = Depends(get_component_query_service),
):
    return await service.get_subsidy_assignments(scheme_id, year_code, subsidy_status)


@router.get("/summary")
async def get_scheme_summary(
    year_code: Optional[int] = Query(None, description="Omit to use current year"),
    service: ComponentQueryService = Depends(get_component_query_service),
):
    return await service.get_scheme_summary(year_code)
