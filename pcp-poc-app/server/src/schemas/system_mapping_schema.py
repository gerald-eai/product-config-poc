from pydantic import BaseModel, ConfigDict
from typing import Optional, Annotated
# from db.models.system_mapping import SystemMappingCurrent, SystemMappingUpdates
from datetime import datetime
from sqlmodel import SQLModel, func, Field, Column, DateTime

# pydantic models
class SystemMappingBase(BaseModel):
    hydraulic_system_name: str
    area_name: str
    region_name: str
    comments: str | None = None
    odmt_area_id: int
    # last_modified: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class SystemMappingUpdatesBase(SystemMappingBase):
    id: int
    date_updated: datetime | None = None


# sql models ie database object
class SystemMapping:
    hydraulic_system_name: str
    area_name: str
    comments: str | None = None
    region_name: str
    odmt_area_id: int

class SystemMappingCurrent(SQLModel, table=True): 
    __tablename__ = "pcp_poc_system_mapping"
    # this changes from DPSN_DEMO in local development to DPSN in production
    __table_args__ = {'schema': 'DPSN_DEMO'}   
    
    hydraulic_system_name: str = Field(primary_key=True, index=True)
    area_name: str
    comments: Optional[str] = Field(default=None)
    region_name: str
    odmt_area_id: int
    
class SystemMappingUpdates(SQLModel, table=True):
    __tablename__ = "pcp_poc_system_mapping_updates"
    __table_args__ = {'schema': 'DPSN_DEMO'}  
    
    id: int = Field(primary_key=True, index=True)
    hydraulic_system_name: Optional[str] = Field(foreign_key="DPSN_DEMO.pcp_poc_system_mapping.hydraulic_system_name")
    area_name: Optional[str]
    comments: Optional[str] 
    region_name: Optional[str]
    odmt_area_id: Optional[int]
    date_updated: Optional[datetime] = Field(default=datetime.now(), sa_column=Column(DateTime(timezone=True)))