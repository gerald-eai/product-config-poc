from sqlmodel import Session, func
from typing import List
from schemas.contact_tank_schema import ContactTankCurrent, ContactTankUpdates
from api.requests.contact_tank_requests import (
    CreateContactTankLive, 
    CreateContactTankRequest,
    UpdateContactTankRequest,
)


class ContactTankRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ContactTankCurrent]:
        return (
            self.db.query(ContactTankCurrent)
            .order_by(ContactTankCurrent.odmt_contact_tank_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_tank_id(self, tank_id: int) -> ContactTankCurrent:
        # return the odmt data based on sres id
        return (
            self.db.query(ContactTankCurrent)
            .filter(ContactTankCurrent.odmt_contact_tank_id == tank_id)
            .first()
        )

    def create_new_entry(self, new_obj: CreateContactTankLive) -> ContactTankCurrent: 
        new_ctank_db = ContactTankCurrent(**vars(new_obj))
        self.db.add(new_ctank_db)
        self.db.flush()
        self.db.commit()
        self.db.refresh(new_ctank_db)
        
        new_ctank_obj = self.get_by_tank_id(new_ctank_db.odmt_contact_tank_id)
        
        return new_ctank_obj


class ContactTankUpdatesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ContactTankUpdates]:
        return (
            self.db.query(ContactTankUpdates)
            .order_by(ContactTankUpdates.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_tank_id(self, tank_id: int) -> ContactTankUpdates:
        return (
            self.db.query(ContactTankUpdates)
            .filter(ContactTankUpdates.odmt_contact_tank_id == tank_id)
            .first()
        )

    def get_by_update_id(self, update_id: int) -> ContactTankUpdates:
        return (
            self.db.query(ContactTankUpdates)
            .filter(ContactTankUpdates.id == update_id)
            .first()
        )

    def create_new_update(self, new_entry: CreateContactTankRequest) -> ContactTankUpdates:
        tank_db_obj = ContactTankUpdates(**vars(new_entry))

        search_db_obj = self.db.query(ContactTankUpdates).filter(ContactTankUpdates.odmt_contact_tank_id == tank_db_obj.odmt_contact_tank_id).all()
        if len(search_db_obj) > 0:
            raise ValueError(f"An entry already exists for Contact Tank Id {tank_db_obj.odmt_contact_tank_id}")
        
        self.db.add(tank_db_obj)
        self.db.flush()
        self.db.commit()
        self.db.refresh(tank_db_obj)

        return tank_db_obj

    def update_existing_entry(
        self, update_id: int, update_entry: UpdateContactTankRequest
    ) -> ContactTankUpdates:
        tank_db_obj = (
            self.db.query(ContactTankUpdates)
            .filter(ContactTankUpdates.id == update_id)
            .first()
        )

        if tank_db_obj is None:
            return None

        for key, value in vars(update_entry).items():
            if value is not None:
                setattr(tank_db_obj, key, value)
        # update the datetime
        setattr(tank_db_obj, "date_updated", func.now())
        # commit the update
        self.db.commit()
        self.db.refresh(tank_db_obj)
        updated_data = (
            self.db.query(ContactTankUpdates)
            .filter(ContactTankUpdates.id == update_id)
            .first()
        )
        return updated_data
