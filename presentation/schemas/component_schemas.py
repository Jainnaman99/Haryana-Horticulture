from pydantic import BaseModel
from typing import Optional, List


class SchemeResponse(BaseModel):
    scheme_id: int
    scheme_code: str
    scheme_name: str
    is_active: bool


class ComponentTypeResponse(BaseModel):
    component_type_id: int
    component_type_code: str
    component_type_name: Optional[str] = None


class ComponentResponse(BaseModel):
    component_id: int
    component_code: str
    component_name: str
    component_type_id: int
    name_hindi: Optional[str] = None


class SubComponentResponse(BaseModel):
    sub_component_id: int
    sub_component_code: str
    sub_component_name: str
    component_id: Optional[int] = None
    name_hindi: Optional[str] = None


class CropItemResponse(BaseModel):
    crop_item_id: int
    crop_item_code: str
    crop_item_name: str
    sub_component_id: Optional[int] = None
    name_hindi: Optional[str] = None


class YearResponse(BaseModel):
    year_id: int
    year_code: int
    year_label: str
    is_current: bool


class SchemeHierarchyResponse(BaseModel):
    scheme_name: str
    scheme_id: int
    component_type_name: Optional[str] = None
    component_type_id: Optional[int] = None
    component_name: Optional[str] = None
    component_id: Optional[int] = None
    sub_component_name: Optional[str] = None
    sub_component_id: Optional[int] = None
    crop_item_name: Optional[str] = None
    crop_item_id: Optional[int] = None
    year_label: Optional[str] = None
    subsidy_status: Optional[str] = None


class CropItemWithStatus(BaseModel):
    crop_item_id: int
    crop_item_name: str
    sub_component_id: Optional[int] = None
    subsidy_status: Optional[str] = None


class CascadeResponse(BaseModel):
    component_types: List[ComponentTypeResponse]
    components: List[ComponentResponse]
    sub_components: List[SubComponentResponse]
    crop_items: List[CropItemWithStatus]


class SubsidyAssignmentResponse(BaseModel):
    scheme_crop_item_id: int
    scheme_name: str
    component_name: Optional[str] = None
    sub_component_name: Optional[str] = None
    crop_item_name: Optional[str] = None
    year_label: str
    subsidy_status: str
    created_at: Optional[str] = None


class SchemeSummaryResponse(BaseModel):
    scheme_name: str
    scheme_id: int
    assigned_count: int
    workflow_active_count: int
    year_label: str
