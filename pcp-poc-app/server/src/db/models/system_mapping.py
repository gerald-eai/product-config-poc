# include the system mapping metadata tables here 
from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint, func
from db.database import Base


class SystemMappingCurrent(Base): 
    __tablename__ = "pcp_poc_system_mapping"
    # this changes from DPSN_DEMO in local development to DPSN in production
    __table_args__ = {'schema': 'DPSN_DEMO'}        
    
    hydraulic_system_name= Column(String, primary_key=True,nullable=False)
    area_name=Column(String, nullable=False)
    region_name=Column(String, nullable=False)
    comments=Column(String)
    odmt_area_id=Column(Integer,nullable=False)
    last_modified=Column(DateTime)
    
class SystemMappingUpdates(Base): 
    __tablename__ = "pcp_poc_system_mapping_updates"
    # this changes from DPSN_DEMO in local development to DPSN in production
    __table_args__ = {'schema': 'DPSN_DEMO'}        
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hydraulic_system_name= Column(String,nullable=False)
    area_name=Column(String)
    region_name=Column(String)
    comments=Column(String)
    odmt_area_id=Column(Integer)
    date_updated=Column(DateTime,default=func.now())
    ForeignKeyConstraint(["hydraulic_system_name"], ["pcp_poc_system_mapping.hydraulic_system_name"])
