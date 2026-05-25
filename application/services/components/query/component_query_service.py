import asyncio
from typing import Optional, List, Dict
from domain.interfaces.components.query.icomponent_query_repository import IComponentQueryRepository


class ComponentQueryService:
    def __init__(self, repo: IComponentQueryRepository):
        self.repo = repo

    async def get_all_schemes(self, is_active: Optional[bool]) -> List[dict]:
        return await self.repo.get_all_schemes(is_active)

    async def get_scheme_by_id(self, scheme_id: int) -> Optional[dict]:
        return await self.repo.get_scheme_by_id(scheme_id)

    async def get_component_types(self, scheme_id: Optional[int], is_active: Optional[bool]) -> List[dict]:
        return await self.repo.get_component_types(scheme_id, is_active)

    async def get_components(self, scheme_id: Optional[int], component_type_id: Optional[int], is_active: Optional[bool]) -> List[dict]:
        return await self.repo.get_components(scheme_id, component_type_id, is_active)

    async def get_sub_components(self, scheme_id: Optional[int], component_id: Optional[int], is_active: Optional[bool]) -> List[dict]:
        return await self.repo.get_sub_components(scheme_id, component_id, is_active)

    async def get_crop_items(self, scheme_id: Optional[int], sub_component_id: Optional[int], is_active: Optional[bool]) -> List[dict]:
        return await self.repo.get_crop_items(scheme_id, sub_component_id, is_active)

    async def get_years(self) -> List[dict]:
        return await self.repo.get_years()

    async def get_scheme_hierarchy(self, scheme_id: int, year_code: int, subsidy_status: Optional[str]) -> List[dict]:
        return await self.repo.get_scheme_hierarchy(scheme_id, year_code, subsidy_status)

    async def get_cascade_by_scheme(self, scheme_id: int, year_code: Optional[int]) -> dict:
        # Fetches all 4 entity lists for this scheme in parallel (one DB round-trip each)
        component_types, components, sub_components, crop_items = await asyncio.gather(
            self.repo.get_component_types(scheme_id, is_active=True),
            self.repo.get_components(scheme_id, component_type_id=None, is_active=True),
            self.repo.get_sub_components(scheme_id, component_id=None, is_active=True),
            self.repo.get_crop_items(scheme_id, sub_component_id=None, is_active=True),
        )
        return {
            "component_types": component_types,
            "components": components,
            "sub_components": sub_components,
            "crop_items": crop_items,
        }

    async def get_subsidy_assignments(self, scheme_id: Optional[int], year_code: int, subsidy_status: Optional[str]) -> List[dict]:
        return await self.repo.get_subsidy_assignments(scheme_id, year_code, subsidy_status)

    async def get_scheme_summary(self, year_code: Optional[int]) -> List[dict]:
        return await self.repo.get_scheme_summary(year_code)
