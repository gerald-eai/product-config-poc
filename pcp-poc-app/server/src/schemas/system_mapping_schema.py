from pydantic import BaseModel, ConfigDict
from typing import Optional, Annotated
from db.models.system_mapping import SystemMappingCurrent, SystemMappingUpdates
from datetime import datetime 

#pydantic models 
class SystemMappingBase(BaseModel):
    hydraulic_system_name: str 
    area_name: str 
    region_name: str 
    comments: str | None = None
    odmt_area_id: int 
    # last_modified: datetime | None = None 
    
    model_config=ConfigDict(from_attributes=True)
    

class SystemMappingUpdatesBase(SystemMappingBase): 
    id: int 
    date_updated: datetime | None = None

# sql models ie database object
class SystemMapping: 
    hydraulic_system_name:str 
    area_name:str 
    comments: str | None = None
    region_name: str
    odmt_area_id: int 
    
    
class SystemMappingCurrent(SystemMapping): 
    last_modified: datetime | None = None 
    
    def __init__(self, sys_map_db: SystemMappingCurrent): 
        self.hydraulic_system_name = sys_map_db.hydraulic_system_name 
        self.area_name = sys_map_db.area_name 
        self.region_name = sys_map_db.region_name 
        self.odmt_area_id = sys_map_db.odmt_area_id 
        self.last_modified = sys_map_db.last_modified 
        self.comments=sys_map_db.comments
        
    @classmethod
    def from_db(cls, sys_map_db: SystemMappingCurrent):
        return cls(sys_map_db)

class SystemMappingUpdate(SystemMapping): 
    id: int 
    date_updated: datetime | None = None 
    
    def __init__(self, sys_map_db: SystemMappingUpdates): 
        self.hydraulic_system_name = sys_map_db.hydraulic_system_name 
        self.area_name = sys_map_db.area_name 
        self.region_name = sys_map_db.region_name 
        self.odmt_area_id = sys_map_db.odmt_area_id 
        self.id = sys_map_db.id 
        self.date_updated = sys_map_db.date_updated
        self.comments=sys_map_db.comments
    
    @classmethod
    def from_db(cls, sys_map_db: SystemMappingUpdates):
        return cls(sys_map_db)
    
