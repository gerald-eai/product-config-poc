from sqlalchemy.orm import Session
from db.audit_log_repository import AuditLogRepository
from schemas.audit_log_schema import AuditLog 
from api.requests.audit_log_requests import CreateAuditRequest
from core.utils import generate_audit_uuid
from typing import List 

class AuditLogService:
    """Responsible for all of our audit log services. 
    
    Attributes: 
        repository (AuditLogRepository): the repository object that is used to perform the CRUD operations.
    """
    def __init__(self, db: Session):
        """initialises our repository attribute

        Args:
            db (Session): session object used for connecting to the database.
        """
        self.repository = AuditLogRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get all CRUD service, returns paginated list of audit log entries

        Args:
            skip (int, optional): Our offset value. Defaults to 0.
            limit (int, optional): Max number of records to return. Defaults to 100.

        Returns:
            List[AuditLog]: List of audit log records
        """
        query = self.repository.get_all(skip, limit)

        return query

    def get_by_event_id(self, event_id: str) -> AuditLog:
        """Get a record entry based on it's event uuid

        Args:
            event_id (str): event id 

        Returns:
            AuditLog: _description_
        """
        query = self.repository.get_by_event_id(event_id)

        return query

    def create_new_event(self, new_event: CreateAuditRequest) -> AuditLog:
        """Creates a new audit event record, and returns the newly created object. 

        Args:
            new_event (CreateAuditRequest): New audit log event to save in the table.

        Returns:
            AuditLog: _description_
        """
        uuid_ = generate_audit_uuid()
        new_event.event_id = uuid_

        new_audit_entry = self.repository.create_event(new_event)

        return new_audit_entry
