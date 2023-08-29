from sqlalchemy.orm import Session
from db.contact_tanks_repository import (
    ContactTankRepository,
    ContactTankUpdatesRepository,
)
from api.requests.contact_tank_requests import (
    CreateContactTankLive, 
    CreateContactTankRequest,
    UpdateContactTankRequest,
)
# from schemas.contact_tank_schema import ContactTankCurrentDB, ContactTankUpdateDB
from schemas.contact_tank_schema import ContactTankCurrent, ContactTankUpdates
from sqlmodel import Session
from typing import List



class ContactTankService:
    def __init__(self, db: Session):
        self.repository = ContactTankRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ContactTankCurrent]:
        query = self.repository.get_all(skip, limit)
        # return [ContactTankCurrentDB.from_db(el) for el in query]
        return query

    def get_by_tank_id(self, tank_id: int) -> ContactTankCurrent:
        query = self.repository.get_by_tank_id(tank_id)
        # return ContactTankCurrentDB.from_db(query)
        return query

    def create_new_entry(self, new_tank: CreateContactTankLive) -> ContactTankCurrent:
        new_ctank_obj = self.repository.create_new_entry(new_tank)
        # return ContactTankCurrentDB.from_db(new_ctank_obj)
        return new_ctank_obj
    
    

class ContactTankUpdateService:
    def __init__(self, db: Session):
        self.repository = ContactTankUpdatesRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ContactTankUpdates]:
        query = self.repository.get_all(skip, limit)
        # return [ContactTankUpdateDB.from_db(el) for el in query]
        return query 

    def get_by_tank_id(self, tank_id: int) -> ContactTankUpdates:
        query = self.repository.get_by_tank_id(tank_id)
        # return ContactTankUpdateDB.from_db(query)
        return query

    def create_new_update(self, new_tank: CreateContactTankRequest) -> ContactTankUpdates:
        new_tank_obj = self.repository.create_new_update(new_entry=new_tank)
        # return ContactTankUpdateDB.from_db(new_tank_obj)
        return new_tank_obj

    def update_existing_entry(
        self, update_id: int, modified_tank: UpdateContactTankRequest
    ) -> ContactTankUpdates:
        modified_tank_obj = self.repository.update_existing_entry(
            update_id, modified_tank
        )
        # return ContactTankUpdateDB.from_db(modified_tank_obj)
        return modified_tank_obj
