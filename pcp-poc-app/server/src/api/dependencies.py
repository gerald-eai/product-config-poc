from services import sres_service
from sqlalchemy.orm import Session
from fastapi import Depends
from db.database import get_db

def get_sres_service(db: Session = Depends(get_db)): 
    return sres_service.SresService(db)

def get_sres_update_service(db: Session = Depends(get_db)): 
    return sres_service.SresUpdatesService(db)
