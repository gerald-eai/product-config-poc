from pydantic import BaseModel, ConfigDict
from typing import Optional, Annotated
from db.models.sres import SresCurrent, SresUpdates
from datetime import datetime


class SresBase(BaseModel): 
    # required params
    odmt_sres_id: int 
    hydraulic_system_name: str 
    sres_name: str
    cell_name: str 
    pi_tag_name: str 
    engineering_unit: str
    # optional params
    operating_level: float | None = None
    bwl: float | None = None
    twl: float | None = None
    capacity: float | None = None
        
    model_config = ConfigDict(from_attributes=True)
    
class SresUpdateBase(BaseModel): 
    # required params
    id: int  
    odmt_sres_id: int 
    hydraulic_system_name: str 
    sres_name: str
    cell_name: str 
    pi_tag_name: str 
    engineering_unit: str
    # optional params
    operating_level: float | None = None
    bwl: float | None = None
    twl: float | None = None
    capacity: float | None = None
    date_updated: datetime | None = None
        
    model_config = ConfigDict(from_attributes=True)
    
    
class Sres: 
    # required params
    odmt_sres_id: int 
    hydraulic_system_name: str 
    sres_name: str
    cell_name: str 
    pi_tag_name: str 
    engineering_unit: str
    # optional params
    operating_level: float | None = None
    bwl: float | None = None
    twl: float | None = None
    capacity: float | None = None
    
    def __repr__(self): 
        return f"SRES ID: {self.odmt_sres_id} \
            Hydraulic System Name: {self.hydraulic_system_name} \
            SRES Name: {self.sres_name} \
            Cell Name: {self.cell_name} \
            PI Tag Name: {self.pi_tag_name} \
            Engineering Unit: {self.engineering_unit}"
    

class SresCurrent(Sres):     
    # optional params 
    last_modified: datetime | None = None 
    def __init__(self, sres_db: SresCurrent): 
        self.odmt_sres_id = sres_db.odmt_sres_id
        self.hydraulic_system_name = sres_db.hydraulic_system_name
        self.sres_name = sres_db.sres_name
        self.cell_name = sres_db.cell_name
        self.pi_tag_name = sres_db.pi_tag_name
        self.engineering_unit = sres_db.engineering_unit
        self.operating_level = sres_db.operating_level
        self.bwl = sres_db.bwl
        self.twl = sres_db.twl
        self.capacity = sres_db.capacity
        self.last_modified = sres_db.last_modified

    @classmethod
    def from_db(cls, sres_db: SresCurrent): 
        return cls(sres_db)
    
class SresUpdate(Sres):
    # required params
    id: int  
    # optional params
    date_updated: datetime | None = None
    
    def __init__(self, sres_db: SresUpdates): 
        self.id = sres_db.id
        self.odmt_sres_id = sres_db.odmt_sres_id
        self.hydraulic_system_name = sres_db.hydraulic_system_name
        self.sres_name = sres_db.sres_name
        self.cell_name = sres_db.cell_name
        self.pi_tag_name = sres_db.pi_tag_name
        self.engineering_unit = sres_db.engineering_unit
        self.operating_level = sres_db.operating_level
        self.bwl = sres_db.bwl
        self.twl = sres_db.twl
        self.capacity = sres_db.capacity
        self.date_updated = sres_db.date_updated
        
    @classmethod
    def from_db(cls, sres_db: SresUpdates): 
        return cls(sres_db)