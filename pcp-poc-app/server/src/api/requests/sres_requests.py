from pydantic import BaseModel
from typing import Optional, Annotated
from datetime import datetime

# payload body for creating a new Sres Entry
class CreateSresUpdate(BaseModel): 
    odmt_sres_id: int
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

# payload body for updating a SresUpdate entry, everything is optional apart from the id 
class UpdateSresUpdate(BaseModel): 
    id: int
    hydraulic_system_name: str | None = None
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
    date_updated: datetime | None = None