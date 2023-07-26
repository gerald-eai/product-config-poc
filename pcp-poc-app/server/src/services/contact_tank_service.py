from db.models.contact_tanks import ContactTanksCurrent, ContactTanksUpdate
from sqlalchemy.orm import Session
from db.contact_tanks_repository import (
    ContactTankRepository,
    ContactTankUpdatesRepository,
)
from api.requests.contact_tank_requests import (
    CreateContactTankRequest,
    UpdateContactTankRequest,
)
from schemas.contact_tank_schema import ContactTankCurrentDB, ContactTankUpdateDB


class ContactTankService:
    def __init__(self, db: Session):
        self.repository = ContactTankRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100):
        query = self.repository.get_all(skip, limit)
        return [ContactTankCurrentDB.from_db(el) for el in query]

    def get_by_tank_id(self, tank_id: int):
        query = self.repository.get_by_tank_id(tank_id)
        return ContactTankCurrentDB.from_db(query)


class ContactTankUpdateService:
    def __init__(self, db: Session):
        self.repository = ContactTankUpdatesRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100):
        query = self.repository.get_all(skip, limit)
        return [ContactTankUpdateDB.from_db(el) for el in query]

    def get_by_tank_id(self, tank_id: int):
        query = self.repository.get_by_tank_id(tank_id)
        return ContactTankUpdateDB.from_db(query)

    def create_new_update(self, new_tank: CreateContactTankRequest):
        new_tank_obj = self.repository.create_new_update(new_entry=new_tank)
        return ContactTankUpdateDB.from_db(new_tank_obj)

    def update_existing_entry(
        self, update_id: int, modified_tank: UpdateContactTankRequest
    ):
        modified_tank_obj = self.repository.update_existing_entry(
            update_id, modified_tank
        )
        return ContactTankUpdateDB.from_db(modified_tank_obj)
