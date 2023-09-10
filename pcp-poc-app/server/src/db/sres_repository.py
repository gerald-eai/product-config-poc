from api.requests.sres_requests import CreateNewSres, UpdateSres
from schemas.sres_schema import SresCurrent
from sqlmodel import Session, func
from typing import List

class SresRepository:
    # repository for current sres data, this is explicitly for current therefore it only performs read operations
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SresCurrent]:
        return (
            self.db.query(SresCurrent)
            .order_by(SresCurrent.odmt_sres_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, sres_id: int) -> SresCurrent:
        # return the odmt data based on sres id
        return (
            self.db.query(SresCurrent)
            .filter(SresCurrent.odmt_sres_id == sres_id)
            .first()
        )
        
    def create_new_entry(self, new_obj: CreateNewSres) -> SresCurrent: 
        print(f"NEW OBJECT TO CREATE: \n{new_obj}")
        sres_current_db = SresCurrent(**vars(new_obj))
        sres_current_db.last_modified = func.now()
        sres_current_db.production_state = "pending"
        
        print(f"Sres Current DB Obj: {sres_current_db}")
        self.db.add(sres_current_db)
        self.db.commit()
        self.db.refresh(sres_current_db)
        new_sres_obj = self.get_by_id(sres_current_db.odmt_sres_id)
        
        return new_sres_obj
    
    def update_existing_entry(self, updated_obj: UpdateSres) -> SresCurrent: 
        sres_db_obj = self.get_by_id(updated_obj.odmt_sres_id)

        if sres_db_obj is None:
            return None

        for key, value in vars(updated_obj).items():
            if value is not None:
                setattr(sres_db_obj, key, value)
        
        # update the datetime and the production state
        setattr(sres_db_obj, "last_modified", func.now())
        setattr(sres_db_obj, "production_state", "pending")
        
        # commit the update
        self.db.commit()
        self.db.refresh(sres_db_obj)
        updated_data = self.get_by_id(updated_obj.odmt_sres_id)
        
        return updated_data 

