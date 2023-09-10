# from db.models.sres import SresCurrent, SresUpdate
from sqlalchemy.orm import Session
from db.sres_repository import SresRepository
from schemas.sres_schema import SresCurrent
from api.requests.sres_requests import CreateNewSres
from typing import List


class SresService:
    """_summary_
    Create & Read from the SRES current entries table
    """

    def __init__(self, db: Session):
        self.repository = SresRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) ->List[SresCurrent]:
        query = self.repository.get_all(skip, limit)

        return query

    def get_by_id(self, sres_id: int) -> SresCurrent:
        query = self.repository.get_by_id(sres_id=sres_id)
        return query
    
    def create_new_entry(self, new_obj: CreateNewSres) -> SresCurrent:
        new_entry = self.repository.create_new_entry(new_obj)
        return new_entry
    
    def update_existing_entry(self, updated_obj: SresCurrent) -> SresCurrent:
        updated_entry = self.repository.update_existing_entry(updated_obj)

        return updated_entry
