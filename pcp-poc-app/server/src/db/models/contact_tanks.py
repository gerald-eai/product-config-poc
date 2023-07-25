from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float, ForeignKeyConstraint, SmallInteger, func
from sqlalchemy.orm import relationship 
from datetime import datetime

from db.database import Base 


class ContactTanksCurrent(Base): 
    __tablename__="pcp_poc_contact_tanks"
    __table_args__={"schema": "DPSN_DEMO"}
    
    odmt_contact_tank_id = Column(Integer, primary_key=True, index=True)
    hydraulic_system_name=Column(String, nullable=False)
    sres_name=Column(String, nullable=False)
    cell_name=Column(String, nullable=False)
    pi_tag_name =Column(String, nullable=False)
    engineering_unit =Column(String, nullable=False)
    validated_tag=Column(String)
    operating_level =Column(Float)
    bwl=Column(Float) 
    twl=Column(Float)
    capacity =Column(Float)
    comments =Column(String) 
    include_SDSR =Column(SmallInteger) 
    include_SRV =Column(SmallInteger) 
    include_WPRO =Column(SmallInteger) 
    last_modified =Column(DateTime)
    ForeignKeyConstraint(["hydraulic_system_name"], ["pcp_poc_system_mapping.hydraulic_system_name"])
    
class ContactTanksUpdate(Base): 
    __tablename__="pcp_poc_contact_tanks_updates"
    __table_args__={"schema": "DPSN_DEMO"}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    odmt_contact_tank_id = Column(Integer)
    hydraulic_system_name=Column(String, nullable=False)
    sres_name=Column(String, nullable=False)
    cell_name=Column(String, nullable=False)
    pi_tag_name =Column(String, nullable=False)
    engineering_unit =Column(String, nullable=False)
    validated_tag=Column(String)
    operating_level =Column(Float)
    bwl=Column(Float) 
    twl=Column(Float)
    capacity =Column(Float)
    comments =Column(String) 
    include_SDSR =Column(SmallInteger) 
    include_SRV =Column(SmallInteger) 
    include_WPRO =Column(SmallInteger) 
    date_updated =Column(DateTime, default=func.now())
    ForeignKeyConstraint(["hydraulic_system_name"], ["pcp_poc_system_mapping.hydraulic_system_name"])
    ForeignKeyConstraint(["odmt_contact_tank_id"], ["pcp_poc_contact_tanks.odmt_contact_tank_id"])
    
    
    
