from pydantic import BaseModel
from typing import Optional


class ComponentTypeDTO(BaseModel):
    component_type_id: int
    component_type_code: str
    component_type_name: Optional[str] = None


class ComponentDTO(BaseModel):
    component_id: int
    component_code: str
    component_name: str
    component_type_id: int
    name_hindi: Optional[str] = None


class SubComponentDTO(BaseModel):
    sub_component_id: int
    sub_component_code: str
    sub_component_name: str
    component_id: Optional[int] = None
    name_hindi: Optional[str] = None


class CropItemDTO(BaseModel):
    crop_item_id: int
    crop_item_code: str
    crop_item_name: str
    sub_component_id: Optional[int] = None
    name_hindi: Optional[str] = None
