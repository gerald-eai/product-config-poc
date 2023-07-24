from db.models.sres import SresCurrent, SresUpdates 
from sqlalchemy.orm import Session 
from sqlalchemy import func
from api.requests.sres_requests import CreateSresUpdate, UpdateSresUpdate
                
class SresRepository(): 
    # repository for current sres data, this is explicitly for current therefore it only performs read operations
    def __init__(self, db: Session): 
        self.db = db
        
    def get_all(self, skip: int = 0, limit: int = 100): 
        return self.db.query(SresCurrent).order_by(SresCurrent.odmt_sres_id).offset(skip).limit(limit).all()
    
    def get_by_id(self, sres_id: int): 
        # return the odmt data based on sres id 
        return self.db.query(SresCurrent).filter(SresCurrent.odmt_sres_id==sres_id).first()
        
class SresUpdatesRepository(): 
    # repository for sres updates, this is explicitly for updates therefore it only performs create and update operations
    def __init__(self, db: Session): 
        self.db = db
        
    def get_all(self, skip, limit): 
        return self.db.query(SresUpdates).order_by(SresCurrent.id).offset(skip).limit(limit).all()
    
    def get_by_sres_id(self, sres_id: int): 
        return self.db.query(SresUpdates).filter(SresUpdates.odmt_sres_id==sres_id).first()

    # def get_by_update_id(self, update_id: int): 
    #     return self.db.query(SresUpdates).filter(SresUpdates.id==update_id).first()
    
    def create_new_update(self, new_entry: CreateSresUpdate):
        sres_update_db = SresUpdates(**new_entry.model_dump())
        # create the new item
        print(f"Our new entry in the db is: {sres_update_db}")
        self.db.add(sres_update_db)
        self.db.flush()
        new_entry_id = sres_update_db.id
        self.db.commit()
        self.db.refresh(sres_update_db)
        print(f"Newly Added Id: {new_entry_id}" )
        return sres_update_db

    def modify_new_update(self, update_id: int, update_entry: UpdateSresUpdate):
        sres_db_item = self.get_by_update_id(update_id)
        # extract all values in the new_entry where it is not null 
        for key,value in update_entry.model_dump().items():
            print(f"Updated Key Value Pairs: {{{key}, {value}}}")
            if value is not None:
                # take the attribute from the db request and set that key to it's new value
                setattr(sres_db_item, key, value)
        # update the datetime
        setattr(sres_db_item, "date_updated", func.now())
        # commit the update
        self.db.commit()
        self.db.refresh(sres_db_item)
        updated_data = self.get_by_update_id(update_id)
        return updated_data