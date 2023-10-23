# Repository for the Audit log
from sqlmodel import Session
from api.requests.audit_log_requests import CreateAuditRequest
from schemas.audit_log_schema import AuditLog
from typing import List


class AuditLogRepository:
    """Responsible for all of our audit log database operations.

    Attributes:
        db (Session): Database connection object
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Returns the paginated list of records from audit log table.

         Args:
            skip (int, optional): Our offset value. Defaults to 0.
            limit (int, optional): Number of records to return per page. Defaults to 100.


        Returns:
            List[AuditLog]: Paginated list of records from the audit log table.
        """
        return (
            self.db.query(AuditLog)
            .order_by(AuditLog.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_event_id(self, event_id: str) -> AuditLog:
        """Returns a record from audit log table that matches the given event_id. 

        Args:
            event_id (str): Audit log event id

        Returns:
            AuditLog: The audit log entry from the database if it exists
        """
        return self.db.query(AuditLog).filter(AuditLog.event_id == event_id).first()

    def create_event(self, new_log: CreateAuditRequest) -> AuditLog:
        """Creates a new Audit log object in the SRES config table.

        Args:
            new_log (CreateAuditRequest): The new audit log object

        Raises:
            ValueError: An error if the event id of the audit log is already within the table. 

        Returns:
            AuditLog: An audit log object that will be stored in the table.
        """
        # create a new entry with data provided
        new_audit_obj = AuditLog(**vars(new_log))

        # check if an entry already exists
        search_db_obj = (
            self.db.query(AuditLog)
            .filter(AuditLog.event_id == new_audit_obj.event_id)
            .all()
        )
        if len(search_db_obj) > 0:
            raise ValueError(
                f"An entry already exists for Event Id: {new_audit_obj.event_id}"
            )

        self.db.add(new_audit_obj)
        self.db.flush()

        self.db.commit()
        self.db.refresh(new_audit_obj)

        return new_audit_obj
