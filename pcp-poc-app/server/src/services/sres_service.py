# from db.models.sres import SresCurrent, SresUpdate
from sqlalchemy.orm import Session
from db.sres_repository import SresRepository, SresUpdatesRepository
from schemas.sres_schema import SresCurrent, SresUpdate
from api.requests.sres_requests import CreateNewSresLive, CreateSresUpdate, UpdateSresUpdate



class SresService:
    """_summary_
    Read from the SRES current entries table
    """

    def __init__(self, db: Session):
        self.repository = SresRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100):
        query = self.repository.get_all(skip, limit)

        # return [SresCurrent.from_db(el) for el in query]
        return query

    def get_by_id(self, sres_id: int):
        query = self.repository.get_by_id(sres_id=sres_id)
        # return SresCurrent.from_db(query)
        return query
    
    def create_new_entry(self, new_obj: CreateNewSresLive):
        new_entry = self.repository.create_new_entry(new_obj)
        # return SresCurrent.from_db(new_entry)
        return new_entry

# create service for updating the contents of the SRES Updates table
class SresUpdatesService:
    """_summary_
    Create, Read, and Update from the SRES Updates table
    """

    def __init__(self, db: Session):
        self.repository = SresUpdatesRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100):
        query = self.repository.get_all(skip, limit)
        # return [SresUpdate.from_db(el) for el in query]
        return query

    def get_by_sres_id(self, sres_id: int):
        query = self.repository.get_by_sres_id(sres_id=sres_id)
        # return SresUpdate.from_db(query)
        return query

    def get_by_update_id(self, update_id: int):
        query = self.repository.get_by_update_id(update_id=update_id)
        # return SresUpdate.from_db(query)
        return query

    def create_new_update(self, sres_updates: CreateSresUpdate):
        print("Create New Update Service")
        new_entry = self.repository.create_new_update(sres_updates)
        # return SresUpdate.from_db(new_entry)
        return new_entry

    def modify_update(self, updated_id: int, updated_entry: UpdateSresUpdate):
        updated_entry = self.repository.modify_new_update(
            update_id=updated_id, update_entry=updated_entry
        )
        # return SresUpdate.from_db(updated_entry)
        return updated_entry
