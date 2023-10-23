# from db.models.sres import SresCurrent, SresUpdate
from sqlalchemy.orm import Session
from db.sres_repository import SresRepository
from schemas.sres_schema import SresCurrent
from api.requests.sres_requests import CreateNewSres
from typing import List


class SresService:
    """Service class that is responsible for the business logic of the SRES API. 
        A layer that is on top of our Repository layer. 
        
        Attributes:
            repository (SresRepository): the repository object that is used to perform the CRUD operations.
    """

    def __init__(self, db: Session):
        """initialises our repository attribute

        Args:
            db (Session): session object used for connecting to the database.
        """
        self.repository = SresRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) ->List[SresCurrent]:
        """Get all CRUD service, returns paginated list of sres entries. 

        Args:
            skip (int, optional): Our offset value. Defaults to 0.
            limit (int, optional): Max number of records to return. Defaults to 100.

        Returns:
            List[SresCurrent]: Paginated list of all SRES records in the table
        """
        query = self.repository.get_all(skip, limit)

        return query

    def get_by_id(self, sres_id: int) -> SresCurrent:
        """Returns a record that matches the sres_id arg

        Args:
            sres_id (int): sres id being queried

        Returns:
            SresCurrent: The Sres object from the database
        """
        query = self.repository.get_by_id(sres_id=sres_id)
        return query
    
    def create_new_entry(self, new_obj: CreateNewSres) -> SresCurrent:
        """Service to create a new SRES object in the SRES config table.

        Args:
            new_obj (CreateNewSres): The new SRES object

        Returns:
            SresCurrent: Sres object that has been added to the table. 
        """
        new_entry = self.repository.create_new_entry(new_obj)
        return new_entry
    
    def update_existing_entry(self, updated_obj: SresCurrent) -> SresCurrent:
        """Updates existing entries found in the current SRES config tables.

        Args:
            updated_obj (UpdateSres): The updated attributes, the odmt_sres_id should match one found in the table
        Returns:
            SresCurrent: The updated object in the SRES config table
        """
        updated_entry = self.repository.update_existing_entry(updated_obj)

        return updated_entry
