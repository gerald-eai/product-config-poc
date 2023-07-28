from pydantic import BaseModel 
from datetime import datetime 


# current schemas 
class SresSchemaRead(BaseModel): 
    odmt_sres_id: int 
    hydraulic_system_name: str 
    hydraulic_system_name: str
    sres_name: str
    cell_name: str
    pi_tag_name: str
    operating_level: float
    bwl: float
    twl: float
    capacity: float
    include_exclude: str
    comments: str
    include_in_dv: int
    turnover_target_lower: float
    turnover_target_upper: float
    sm_record_id: str
    validated_tag: str
    engineering_unit: str
    date_updated: datetime | None = None