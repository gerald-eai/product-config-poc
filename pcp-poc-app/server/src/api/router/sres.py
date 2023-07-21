# API Endpoints for SRES based requests 
from fastapi import APIRouter, Depends
from db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/sres")

@router.get("")
def get_sres_home(db_conn: Session = Depends(get_db)):
    
    return {"message": "Welcome to the SRES API"} 