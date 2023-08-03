from db.models.sres import SresCurrent, SresUpdates
from sqlalchemy.orm import Session
from sqlalchemy import func
from api.requests.sres_requests import CreateNewSresLive, CreateSresUpdate, UpdateSresUpdate


class SresRepository:
    # repository for current sres data, this is explicitly for current therefore it only performs read operations
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return (
            self.db.query(SresCurrent)
            .order_by(SresCurrent.odmt_sres_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, sres_id: int):
        # return the odmt data based on sres id
        return (
            self.db.query(SresCurrent)
            .filter(SresCurrent.odmt_sres_id == sres_id)
            .first()
        )
        
    def create_new_entry(self, new_obj: CreateNewSresLive): 
        sres_current_db = SresCurrent(**new_obj.model_dump())
        sres_current_db.last_modified = func.now()
        print(f"Sres Current DB Obj: {sres_current_db}")
        self.db.add(sres_current_db)
        self.db.commit()
        self.db.refresh(sres_current_db)
        new_sres_obj = self.get_by_id(sres_current_db.odmt_sres_id)
        
        return new_sres_obj
    

class SresUpdatesRepository:
    # repository for sres updates, this is explicitly for updates therefore it only performs create and update operations
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip, limit):
        return (
            self.db.query(SresUpdates)
            .order_by(SresUpdates.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_sres_id(self, sres_id: int):
        return (
            self.db.query(SresUpdates)
            .filter(SresUpdates.odmt_sres_id == sres_id)
            .first()
        )

    def get_by_update_id(self, update_id: int):
        return self.db.query(SresUpdates).filter(SresUpdates.id == update_id).first()

    def create_new_update(self, new_entry: CreateSresUpdate):
        sres_update_db = SresUpdates(**new_entry.model_dump())
        
        # check if an entry already exists 
        search_db_obj = self.db.query(SresUpdates).filter(SresUpdates.odmt_sres_id == sres_update_db.odmt_sres_id).all()
        if len(search_db_obj) > 0:
            raise ValueError(f"An entry already exists for sres id {sres_update_db.odmt_sres_id}")
        
        self.db.add(sres_update_db)
        # self.db.flush()
        self.db.commit()
        self.db.refresh(sres_update_db)
        new_sres_obj = self.get_by_update_id(sres_update_db.id)
        return new_sres_obj

    def modify_new_update(self, update_id: int, update_entry: UpdateSresUpdate):
        sres_db_obj = self.get_by_update_id(update_id)

        if sres_db_obj is None:
            return None

        for key, value in update_entry.model_dump().items():
            if value is not None:
                setattr(sres_db_obj, key, value)
        # update the datetime
        setattr(sres_db_obj, "date_updated", func.now())
        # commit the update
        self.db.commit()
        self.db.refresh(sres_db_obj)
        updated_data = self.get_by_update_id(update_id)
        return updated_data
