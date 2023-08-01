from db.models.contact_tanks import ContactTanksCurrent, ContactTanksUpdate
from sqlalchemy.orm import Session
from sqlalchemy import func
from api.requests.contact_tank_requests import (
    CreateContactTankLive, 
    CreateContactTankRequest,
    UpdateContactTankRequest,
)


class ContactTankRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return (
            self.db.query(ContactTanksCurrent)
            .order_by(ContactTanksCurrent.odmt_contact_tank_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_tank_id(self, tank_id: int):
        # return the odmt data based on sres id
        return (
            self.db.query(ContactTanksCurrent)
            .filter(ContactTanksCurrent.odmt_contact_tank_id == tank_id)
            .first()
        )

    def create_new_entry(self, new_obj: CreateContactTankLive): 
        new_ctank_db = ContactTanksCurrent(**new_obj.model_dump())
        self.db.add(new_ctank_db)
        self.db.flush()
        self.db.commit()
        self.db.refresh(new_ctank_db)
        
        new_ctank_obj = self.get_by_tank_id(new_ctank_db.odmt_contact_tank_id)
        
        return new_ctank_obj


class ContactTankUpdatesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return (
            self.db.query(ContactTanksUpdate)
            .order_by(ContactTanksUpdate.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_tank_id(self, tank_id: int):
        return (
            self.db.query(ContactTanksUpdate)
            .filter(ContactTanksUpdate.odmt_contact_tank_id == tank_id)
            .first()
        )

    def get_by_update_id(self, update_id: int):
        return (
            self.db.query(ContactTanksUpdate)
            .filter(ContactTanksUpdate.id == update_id)
            .first()
        )

    def create_new_update(self, new_entry: CreateContactTankRequest):
        tank_db_obj = ContactTanksUpdate(**new_entry.model_dump())
        # check if an entry already exists 
        search_db_obj = self.db.query(ContactTanksUpdate).filter(ContactTanksUpdate.odmt_contact_tank_id == tank_db_obj.odmt_contact_tank_id).all()
        if len(search_db_obj) > 0:
            raise ValueError(f"An entry already exists for Contact Tank Id {tank_db_obj.odmt_contact_tank_id}")
        
        self.db.add(tank_db_obj)
        self.db.flush()
        self.db.commit()
        self.db.refresh(tank_db_obj)

        return tank_db_obj

    def update_existing_entry(
        self, update_id: int, update_entry: UpdateContactTankRequest
    ):
        tank_db_obj = (
            self.db.query(ContactTanksUpdate)
            .filter(ContactTanksUpdate.id == update_id)
            .first()
        )

        if tank_db_obj is None:
            return None

        for key, value in update_entry.model_dump().items():
            if value is not None:
                setattr(tank_db_obj, key, value)
        # update the datetime
        setattr(tank_db_obj, "date_updated", func.now())
        # commit the update
        self.db.commit()
        self.db.refresh(tank_db_obj)
        updated_data = (
            self.db.query(ContactTanksUpdate)
            .filter(ContactTanksUpdate.id == update_id)
            .first()
        )
        return updated_data
