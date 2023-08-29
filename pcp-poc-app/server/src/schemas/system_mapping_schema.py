from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, DateTime


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
    
#     def __repr__(self):
#         values = ', '.join([f"{column.name}='{getattr(self, column.name)}'" for column in self.__table__.columns])
#         return f"{self.__class__.__name__}({values})"