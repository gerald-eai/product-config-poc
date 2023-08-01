from pydantic import BaseModel
from typing import Optional, Annotated
from datetime import datetime

class CreateNewSystemMapLive(BaseModel): 
    hydraulic_system_name: str
    area_name: str
    region_name: str 
    odmt_area_id: int
    
    comments: str | None = None
    last_modified: datetime | None = None
    
class CreateSystemMapUpdate(BaseModel):
    hydraulic_system_name: str
    area_name: str | None = None 
    region_name: str | None = None
    comments: str | None = None
    odmt_area_id: int| None = None
    date_updated: datetime | None = None


class UpdateSystemMapUpdate(BaseModel):
    id: int
    hydraulic_system_name: str | None = None
    area_name: str | None = None
    region_name: str | None = None
    comments: str | None = None
    odmt_area_id: int | None = None
    date_updated: datetime | None = None
