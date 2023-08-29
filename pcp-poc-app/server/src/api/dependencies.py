from services import sres_service, system_mapping_service, contact_tank_service, audit_log_service
from sqlalchemy.orm import Session
from fastapi import Depends
from db.session import get_session # sqlmodel 

def get_sres_service(db: Session = Depends(get_session)): 
    return sres_service.SresService(db)

def get_sres_update_service(db: Session = Depends(get_session)): 
    return sres_service.SresUpdatesService(db)

def get_sys_map_service(db: Session = Depends(get_session)): 
    return system_mapping_service.SystemMappingService(db)

def get_sys_map_update_service(db: Session = Depends(get_session)): 
    return system_mapping_service.SystemMappingUpdateService(db)

def get_contact_tank_service(db: Session = Depends(get_session)): 
    return contact_tank_service.ContactTankService(db)

def get_contact_tank_update_service(db: Session = Depends(get_session)):
    return contact_tank_service.ContactTankUpdateService(db)

def get_audit_log_service(db: Session = Depends(get_session)): 
    return audit_log_service.AuditLogService(db)
