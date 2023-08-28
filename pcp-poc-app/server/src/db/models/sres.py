from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float, ForeignKeyConstraint, SmallInteger, func
from sqlalchemy.orm import relationship 
from db.database import Base 

# from sqlmodel import ForeignKeyConstraint, ForeignKey, Field, Session, Integer, DateTime, String, SmallInteger, func 

class SresCurrent(Base): 
    __tablename__="pcp_poc_sres"
    __table_args__={"schema": "DPSN_DEMO"}
    
    odmt_sres_id=Column(Integer, primary_key=True, autoincrement=True, index=True)
    hydraulic_system_name=Column(String, nullable=False)
    sres_name=Column(String, nullable=False)
    cell_name=Column(String, nullable=False)
    pi_tag_name =Column(String, nullable=False)
    engineering_unit =Column(String, nullable=False)
    
    operating_level =Column(Float)
    bwl =Column(Float)
    twl =Column(Float)
    capacity =Column(Float)
    include_exclude =Column(String)
    comments =Column(String)
    include_in_dv =Column(SmallInteger)
    turnover_target_lower =Column(Float)
    turnover_target_upper =Column(Float) 
    sm_record_id =Column(String)
    validated_tag =Column(String)
    last_modified =Column(DateTime)
    ForeignKeyConstraint(["hydraulic_system_name"], ["pcp_poc_system_mapping.hydraulic_system_name"])
    
    def __repr__(self):
        values = ', '.join([f"{column.name}='{getattr(self, column.name)}'" for column in self.__table__.columns])
        return f"{self.__class__.__name__}({values})"
    

class SresUpdates(Base): 
    __tablename__="pcp_poc_sres_updates"
    __table_args__={"schema": "DPSN_DEMO"}
    id =Column(Integer, primary_key=True, index=True, autoincrement=True)
    odmt_sres_id =Column(Integer, nullable=False)
    hydraulic_system_name =Column(String, nullable=False)
    sres_name =Column(String, nullable=False)
    cell_name =Column(String, nullable=False)
    pi_tag_name =Column(String, nullable=False)
    operating_level =Column(Float)
    bwl =Column(Float)
    twl =Column(Float)
    capacity =Column(Float)
    include_exclude =Column(String)
    comments =Column(String)
    include_in_dv =Column(SmallInteger)
    turnover_target_lower =Column(Float)
    turnover_target_upper =Column(Float) 
    sm_record_id =Column(String)
    validated_tag =Column(String)
    engineering_unit =Column(String, nullable=False)
    date_updated =Column(DateTime,default=func.now())
    ForeignKeyConstraint(["hydraulic_system_name"], ["pcp_poc_system_mapping.hydraulic_system_name"])
    ForeignKeyConstraint(["odmt_sres_id"], ["pcp_poc_sres.odmt_sres_id"])
    
    def __repr__(self):
        values = ', '.join([f"{column.name}='{getattr(self, column.name)}'" for column in self.__table__.columns])
        return f"{self.__class__.__name__}({values})"
    
    
