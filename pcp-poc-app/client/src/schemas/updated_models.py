from pydantic import BaseModel 
from datetime import datetime

class UpdateSystemMapUpdate(BaseModel):
    id: int
    hydraulic_system_name: str | None = None
    area_name: str | None = None
    region_name: str | None = None
    comments: str | None = None
    odmt_area_id: int | None = None
    date_updated: datetime | None = None
    
    