from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from domain.interfaces.components.query.icomponent_query_repository import IComponentQueryRepository
from config.sp_caller import exec_sp, exec_sp_one


class ComponentQueryRepository(IComponentQueryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_schemes(self, is_active: Optional[bool]) -> List[dict]:
        params = {}
        if is_active is not None:
            params["is_active"] = 1 if is_active else 0
        return await exec_sp(self.session, "usp_GetAllSchemes", params)

    async def get_scheme_by_id(self, scheme_id: int) -> Optional[dict]:
        return await exec_sp_one(self.session, "usp_GetSchemeById", {"scheme_id": scheme_id})

    async def get_component_types(self, scheme_id: Optional[int], is_active: Optional[bool]) -> List[dict]:
        params = {}
        if scheme_id is not None:
            params["scheme_id"] = scheme_id
        if is_active is not None:
            params["is_active"] = 1 if is_active else 0
        return await exec_sp(self.session, "usp_GetComponentTypes", params)

    async def get_components(self, scheme_id: Optional[int], component_type_id: Optional[int], is_active: Optional[bool]) -> List[dict]:
        params = {}
        if scheme_id is not None:
            params["scheme_id"] = scheme_id
        if component_type_id is not None:
            params["component_type_id"] = component_type_id
        if is_active is not None:
            params["is_active"] = 1 if is_active else 0
        return await exec_sp(self.session, "usp_GetComponents", params)

    async def get_sub_components(self, scheme_id: Optional[int], component_id: Optional[int], is_active: Optional[bool]) -> List[dict]:
        params = {}
        if scheme_id is not None:
            params["scheme_id"] = scheme_id
        if component_id is not None:
            params["component_id"] = component_id
        if is_active is not None:
            params["is_active"] = 1 if is_active else 0
        return await exec_sp(self.session, "usp_GetSubComponents", params)

    async def get_crop_items(self, scheme_id: Optional[int], sub_component_id: Optional[int], is_active: Optional[bool]) -> List[dict]:
        params = {}
        if scheme_id is not None:
            params["scheme_id"] = scheme_id
        if sub_component_id is not None:
            params["sub_component_id"] = sub_component_id
        if is_active is not None:
            params["is_active"] = 1 if is_active else 0
        return await exec_sp(self.session, "usp_GetCropItems", params)

    async def get_years(self) -> List[dict]:
        return await exec_sp(self.session, "usp_GetYears", {})

    async def get_scheme_hierarchy(self, scheme_id: int, year_code: int, subsidy_status: Optional[str]) -> List[dict]:
        params: dict = {"scheme_id": scheme_id, "year_code": year_code}
        if subsidy_status is not None:
            params["subsidy_status"] = subsidy_status
        return await exec_sp(self.session, "usp_GetSchemeHierarchy", params)

    async def get_subsidy_assignments(self, scheme_id: Optional[int], year_code: int, subsidy_status: Optional[str]) -> List[dict]:
        params: dict = {"year_code": year_code}
        if scheme_id is not None:
            params["scheme_id"] = scheme_id
        if subsidy_status is not None:
            params["subsidy_status"] = subsidy_status
        return await exec_sp(self.session, "usp_GetSubsidyAssignments", params)

    async def get_scheme_summary(self, year_code: Optional[int]) -> List[dict]:
        params = {}
        if year_code is not None:
            params["year_code"] = year_code
        return await exec_sp(self.session, "usp_GetSchemeSummary", params)
