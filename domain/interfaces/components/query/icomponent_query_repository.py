from abc import ABC, abstractmethod
from typing import Optional, List


class IComponentQueryRepository(ABC):

    @abstractmethod
    async def get_all_schemes(self, is_active: Optional[bool]) -> List[dict]: pass

    @abstractmethod
    async def get_scheme_by_id(self, scheme_id: int) -> Optional[dict]: pass

    @abstractmethod
    async def get_component_types(self, scheme_id: Optional[int], is_active: Optional[bool]) -> List[dict]: pass

    @abstractmethod
    async def get_components(self, scheme_id: Optional[int], component_type_id: Optional[int], is_active: Optional[bool]) -> List[dict]: pass

    @abstractmethod
    async def get_sub_components(self, scheme_id: Optional[int], component_id: Optional[int], is_active: Optional[bool]) -> List[dict]: pass

    @abstractmethod
    async def get_crop_items(self, scheme_id: Optional[int], sub_component_id: Optional[int], is_active: Optional[bool]) -> List[dict]: pass

    @abstractmethod
    async def get_years(self) -> List[dict]: pass

    @abstractmethod
    async def get_scheme_hierarchy(self, scheme_id: int, year_code: int, subsidy_status: Optional[str]) -> List[dict]: pass

    @abstractmethod
    async def get_subsidy_assignments(self, scheme_id: Optional[int], year_code: int, subsidy_status: Optional[str]) -> List[dict]: pass

    @abstractmethod
    async def get_scheme_summary(self, year_code: Optional[int]) -> List[dict]: pass
