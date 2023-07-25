from sqlalchemy.orm import Session 
from sqlalchemy import func
from db.models.system_mapping import SystemMappingCurrent, SystemMappingUpdates
from api.requests.system_mapping_requests import CreateSystemMapUpdate, UpdateSystemMapUpdate

class SystemMappingRepository(): 
    def __init__(self, db: Session): 
        self.db = db
    
    def get_all(self, skip: int=0, limit: int=100): 
        return self.db.query(SystemMappingCurrent).order_by(SystemMappingCurrent.hydraulic_system_name).offset(skip).limit(limit).all()
    
    def get_by_hydraulic_name(self, hydraulic_name: str): 
        return self.db.query(SystemMappingCurrent).filter(SystemMappingCurrent.hydraulic_system_name == hydraulic_name).first()
    

class SystemMappingUpdatesRepository():
    def __init__(self, db: Session): 
        self.db = db
    
    def get_all(self, skip: int=0, limit: int=100): 
        return self.db.query(SystemMappingUpdates).order_by(SystemMappingUpdates.hydraulic_system_name).offset(skip).limit(limit).all()
    
    def get_by_hydraulic_name(self, hydraulic_name: str): 
        return self.db.query(SystemMappingUpdates).filter(SystemMappingUpdates.hydraulic_system_name == hydraulic_name).first()
    
    def create_new_update(self, new_entry: CreateSystemMapUpdate): 
        sys_map_db_obj = SystemMappingUpdates(**new_entry.model_dump())
        
        self.db.add(sys_map_db_obj)
        self.db.flush()
        db_obj_id = sys_map_db_obj.id
        print(f"Newly added index: {db_obj_id}")
        self.db.commit()
        self.db.refresh(sys_map_db_obj)

        return sys_map_db_obj
    
    def updated_existing_entry(self, update_id: int, update_entry: UpdateSystemMapUpdate): 
        sys_map_db_obj = self.db.query(SystemMappingUpdates).filter(SystemMappingUpdates.id == update_id).first()
        
        if sys_map_db_obj: 
            for key, value in update_entry.model_dump().items(): 
                if value is not None: 
                    setattr(sys_map_db_obj, key, value)
            setattr(sys_map_db_obj, "date_updated", func.now())
            self.db.commit()
            self.db.refresh(sys_map_db_obj)
            updated_db_obj = self.db.query(SystemMappingUpdates).filter(SystemMappingUpdates.id == update_id).first()
            return updated_db_obj
        else: 
            return None