from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateNewSresLive(BaseModel): 
    hydraulic_system_name: str
    sres_name: str
    cell_name: str
    pi_tag_name: str
    engineering_unit: str
    
    operating_level: Optional[float] 
    bwl: Optional[float] 
    twl: Optional[float] 
    capacity: Optional[float] 
    include_exclude: Optional[str] 
    comments: Optional[str]
    include_in_dv: Optional[int] 
    turnover_target_lower: Optional[float] 
    turnover_target_upper: Optional[float] 
    sm_record_id: Optional[str] 
    validated_tag: Optional[str]
    
    last_modified: Optional[datetime]
    
# payload body for creating a new Sres Entry
class CreateSresUpdate(BaseModel):
    odmt_sres_id: int
    hydraulic_system_name: str
    sres_name: str
    cell_name: str
    pi_tag_name: str
    engineering_unit: str
    
    operating_level: Optional[float] 
    bwl: Optional[float] 
    twl: Optional[float] 
    capacity: Optional[float] 
    include_exclude: Optional[str] 
    comments: Optional[str]
    include_in_dv: Optional[int] 
    turnover_target_lower: Optional[float] 
    turnover_target_upper: Optional[float] 
    sm_record_id: Optional[str] 
    validated_tag: Optional[str]
    
    date_updated: Optional[datetime]


# payload body for updating a SresUpdate entry, everything is optional apart from the id
class UpdateSresUpdate(BaseModel):
    id: int
    hydraulic_system_name: Optional[str]
    sres_name: Optional[str]
    cell_name: Optional[str]
    pi_tag_name: Optional[str]
    operating_level: Optional[float]
    bwl: Optional[float]
    twl: Optional[float]
    capacity: Optional[float]
    include_exclude: Optional[str]
    comments: Optional[str]
    include_in_dv: Optional[int]
    turnover_target_lower: Optional[float]
    turnover_target_upper: Optional[float]
    sm_record_id: Optional[str]
    validated_tag: Optional[str]
    date_updated: Optional[datetime]
