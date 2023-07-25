from pydantic import BaseModel, ConfigDict
from typing import Optional, Annotated
from db.models.contact_tanks import ContactTanksCurrent, ContactTanksUpdate
from datetime import datetime


# pydantic models
class ContactTankBase(BaseModel):
    odmt_contact_tank_id: int
    hydraulic_system_name: str
    sres_name: str
    cell_name: str
    pi_tag_name: str
    engineering_unit: str 

    validated_tag: str | None = None
    operating_level: float | None = None
    bwl: float | None = None
    twl: float | None = None
    capacity: float | None = None
    comments: str | None = None
    include_SDSR: int | None = None
    include_SRV: int | None = None
    include_WPRO: int | None = None

    model_config = ConfigDict(from_attributes=True)


class ContactTankCurrentBase(ContactTankBase):
    last_modified: datetime | None = None


class ContactTankUpdateBase(ContactTankBase):
    id: int
    date_updated: datetime | None = None


class ContactTank:
    odmt_contact_tank_id: int
    hydraulic_system_name: str
    sres_name: str
    cell_name: str
    pi_tag_name: str
    engineering_unit: str

    validated_tag: str | None = None
    operating_level: float | None = None
    bwl: float | None = None
    twl: float | None = None
    capacity: float | None = None
    comments: str | None = None
    include_SDSR: int | None = None
    include_SRV: int | None = None
    include_WPRO: int | None = None


class ContactTankCurrentDB(ContactTank):
    last_modified: datetime | None = None

    def __init__(self, tank_db: ContactTanksCurrent):
        self.odmt_contact_tank_id = tank_db.odmt_contact_tank_id
        self.hydraulic_system_name = tank_db.hydraulic_system_name
        self.sres_name = tank_db.sres_name
        self.cell_name = tank_db.cell_name
        self.pi_tag_name = tank_db.pi_tag_name
        self.engineering_unit = tank_db.engineering_unit
        self.validated_tag = tank_db.validated_tag
        self.operating_level = tank_db.operating_level
        self.bwl = tank_db.bwl
        self.twl = tank_db.twl
        self.capacity = tank_db.capacity
        self.comments = tank_db.comments
        self.include_SDSR = tank_db.include_SDSR
        self.include_SRV = tank_db.include_SRV
        self.include_WPRO = tank_db.include_WPRO

    @classmethod
    def from_db(cls, tank_db: ContactTanksCurrent):
        return cls(tank_db)


class ContactTankUpdateDB(ContactTank):
    id: int
    date_updated: datetime | None = None

    def __init__(self, tank_db: ContactTanksUpdate):
        self.id = tank_db.id
        self.odmt_contact_tank_id = tank_db.odmt_contact_tank_id
        self.hydraulic_system_name = tank_db.hydraulic_system_name
        self.sres_name = tank_db.sres_name
        self.cell_name = tank_db.cell_name
        self.pi_tag_name = tank_db.pi_tag_name
        self.engineering_unit = tank_db.engineering_unit
        self.validated_tag = tank_db.validated_tag
        self.operating_level = tank_db.operating_level
        self.bwl = tank_db.bwl
        self.twl = tank_db.twl
        self.capacity = tank_db.capacity
        self.comments = tank_db.comments
        self.include_SDSR = tank_db.include_SDSR
        self.include_SRV = tank_db.include_SRV
        self.include_WPRO = tank_db.include_WPRO
        self.date_updated = tank_db.date_updated
        

    @classmethod
    def from_db(cls, tank_db: ContactTanksUpdate):
        return cls(tank_db)
