from pydantic import BaseModel 
from datetime import datetime 

# Base Class
class BaseRequest(BaseModel): 
    hydraulic_system_name: str
    sres_name: str | None = None 
    cell_name: str | None = None 
    pi_tag_name: str | None = None 
    operating_level: float | None = None
    bwl: float | None = None
    twl: float | None = None
    capacity: float | None = None
    include_exclude: str | None = None
    comments: str | None = None
    include_in_dv: int | None = None
    turnover_target_lower: float | None = None
    turnover_target_upper: float | None = None
    sm_record_id: str | None = None
    validated_tag: str | None = None
    engineering_unit: str | None = None
    
class CreateNewLiveEntry(BaseModel): 
    hydraulic_system_name: str
    sres_name: str
    cell_name: str
    pi_tag_name: str 
    engineering_unit: str
    
    operating_level: float | None = None
    bwl: float | None = None
    twl: float | None = None
    capacity: float | None = None
    include_exclude: str | None = None
    comments: str | None = None
    include_in_dv: int | None = None
    turnover_target_lower: float | None = None
    turnover_target_upper: float | None = None
    sm_record_id: str | None = None
    validated_tag: str | None = None
    
    last_modified: datetime | None = None
    
class CreateNewStagedEntry(BaseRequest): 
    # add in required entries
    odmt_sres_id: int # required foreign key
    date_updated: datetime | None = None

class UpdateStagedEntry(CreateNewStagedEntry): 
    id: int # required primary key
    