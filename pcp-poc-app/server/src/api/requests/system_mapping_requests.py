from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateNewSystemMapLive(BaseModel): 
    hydraulic_system_name: str
    area_name: str
    region_name: str 
    odmt_area_id: int
    
    comments: Optional[str]
    last_modified: Optional[datetime]
    
class CreateSystemMapUpdate(BaseModel):
    hydraulic_system_name: str
    area_name: Optional[str] 
    region_name: Optional[str]
    comments: Optional[str]
    odmt_area_id: Optional[int]
    date_updated: Optional[datetime]


class UpdateSystemMapUpdate(BaseModel):
    id: int
    hydraulic_system_name: Optional[str]
    area_name: Optional[str]
    region_name: Optional[str]
    comments: Optional[str]
    odmt_area_id: Optional[int]
    date_updated: Optional[datetime]
