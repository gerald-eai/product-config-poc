from services import sres_service, system_mapping_service
from sqlalchemy.orm import Session
from fastapi import Depends
from db.database import get_db

def get_sres_service(db: Session = Depends(get_db)): 
    return sres_service.SresService(db)

def get_sres_update_service(db: Session = Depends(get_db)): 
    return sres_service.SresUpdatesService(db)

def get_sys_map_service(db: Session = Depends(get_db)): 
    return system_mapping_service.SystemMappingService(db)

def get_sys_map_update_service(db: Session = Depends(get_db)): 
    return system_mapping_service.SystemMappingUpdateService(db)
