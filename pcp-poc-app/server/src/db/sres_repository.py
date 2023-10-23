from api.requests.sres_requests import CreateNewSres, UpdateSres
from schemas.sres_schema import SresCurrent
from sqlmodel import Session, func
from typing import List

class SresRepository:
    """repository for current sres data, this is explicitly for current therefore it only performs read operations
    Makes use of the Sres ORM objects: SresCurrent, CreateNewSres, UpdateSres
    
    Attributes: 
        db (Session): the database session object
    """
    def __init__(self, db: Session):
        """Initialise the database session object

        Args:
            db (Session): database session object
        """
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SresCurrent]:
        """Returns the paginated list of records from sres table.

        Args:
            skip (int, optional): Our offset value. Defaults to 0.
            limit (int, optional): Number of records to return per page. Defaults to 100.

        Returns:
            List[SresCurrent]: List of records from sres table, 
        """
        return (
            self.db.query(SresCurrent)
            .order_by(SresCurrent.odmt_sres_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, sres_id: int) -> SresCurrent:
        """Returns a record from the SRES config table, based on the sres_id

        Args:
            sres_id (int): sres id that is being queried

        Returns:
            SresCurrent: ORM object
        """
        return (
            self.db.query(SresCurrent)
            .filter(SresCurrent.odmt_sres_id == sres_id)
            .first()
        )
        
    def create_new_entry(self, new_obj: CreateNewSres) -> SresCurrent: 
        """Creates a new SRES object in the SRES config table.
            Every new SRES object is created with production_state set to 'pending'

        Args:
            new_obj (CreateNewSres): The new SRES object

        Returns:
            SresCurrent: Sres object that has been added to the table. 
        """
        sres_current_db = SresCurrent(**vars(new_obj))
        sres_current_db.last_modified = func.now()
        sres_current_db.production_state = "pending"
        
        self.db.add(sres_current_db)
        self.db.commit()
        self.db.refresh(sres_current_db)
        new_sres_obj = self.get_by_id(sres_current_db.odmt_sres_id)
        
        return new_sres_obj
    
    def update_existing_entry(self, updated_obj: UpdateSres) -> SresCurrent: 
        """Updates existing entries found in the current SRES config tables.

        Args:
            updated_obj (UpdateSres): The updated attributes, the odmt_sres_id should match one found in the table
        Returns:
            SresCurrent: The updated object in the SRES config table
        """
        sres_db_obj = self.get_by_id(updated_obj.odmt_sres_id)

        if sres_db_obj is None:
            return None

        for key, value in vars(updated_obj).items():
            if value is not None:
                setattr(sres_db_obj, key, value)
        
        # update the datetime and the production state
        setattr(sres_db_obj, "last_modified", func.now())
        setattr(sres_db_obj, "production_state", "pending")
        
        # commit the update
        self.db.commit()
        self.db.refresh(sres_db_obj)
        updated_data = self.get_by_id(updated_obj.odmt_sres_id)
        
        return updated_data 

