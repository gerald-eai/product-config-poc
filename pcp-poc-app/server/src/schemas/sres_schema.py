from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from typing import Optional
from sqlalchemy import DateTime


class SresCurrent(SQLModel, table=True):
    __tablename__="pcp_poc_sres"
    __table_args__={"schema": "DPSN"}
    
    odmt_sres_id: int = Field(primary_key=True, index=True) 
    hydraulic_system_name: str = Field(foreign_key="DPSN.pcp_poc_system_mapping.hydraulic_system_name")
    sres_name: str
    cell_name: str 
    pi_tag_name: str 
    engineering_unit: str
    
    # optional params
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
    
    def __repr__(self): 
        return f"SRES ID: {self.odmt_sres_id} \
            Hydraulic System Name: {self.hydraulic_system_name} \
            SRES Name: {self.sres_name} \
            Cell Name: {self.cell_name} \
            PI Tag Name: {self.pi_tag_name} \
            Engineering Unit: {self.engineering_unit}"

#     def __repr__(self):
#         values = ', '.join([f"{column.name}='{getattr(self, column.name)}'" for column in self.__table__.columns])
#         return f"{self.__class__.__name__}({values})"

class SresUpdate(SQLModel, table=True): 
    __tablename__="pcp_poc_sres_updates"
    __table_args__={"schema": "DPSN"}
    
    id: int=Field(primary_key=True, index=True)
    odmt_sres_id: int = Field(index=True, foreign_key="DPSN.pcp_poc_sres.odmt_sres_id") 
    hydraulic_system_name: str = Field(foreign_key="DPSN.pcp_poc_system_mapping.hydraulic_system_name")
    
    sres_name: Optional[str]
    cell_name: Optional[str] 
    pi_tag_name: Optional[str] 
    engineering_unit: Optional[str]
    
    # optional params
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
    date_updated: Optional[datetime] = Field(default=datetime.now(), sa_column=Column(DateTime(timezone=True)))
    
    def __repr__(self): 
        return f"SRES ID: {self.odmt_sres_id} \
            Hydraulic System Name: {self.hydraulic_system_name} \
            SRES Name: {self.sres_name} \
            Cell Name: {self.cell_name} \
            PI Tag Name: {self.pi_tag_name} \
            Engineering Unit: {self.engineering_unit}"

#     def __repr__(self):
#         values = ', '.join([f"{column.name}='{getattr(self, column.name)}'" for column in self.__table__.columns])
#         return f"{self.__class__.__name__}({values})"