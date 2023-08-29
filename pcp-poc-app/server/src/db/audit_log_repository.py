# Repository for the Audit log
from sqlalchemy.orm import Session
from api.requests.audit_log_requests import CreateAuditRequest
from schemas.audit_log_schema import AuditLog
from typing import List


class AuditLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return (
            self.db.query(AuditLog)
            .order_by(AuditLog.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_event_id(self, event_id: str) -> AuditLog:
        return self.db.query(AuditLog).filter(AuditLog.event_id == event_id).first()

    def create_event(self, new_log: CreateAuditRequest) -> AuditLog:
        # create a new entry with data provided
        print("The new Audit Entry: \n",new_log)
        new_audit_obj = AuditLog(**vars(new_log))
        
        # check if an entry already exists 
        search_db_obj = self.db.query(AuditLog).filter(AuditLog.event_id == new_audit_obj.event_id).all()
        if len(search_db_obj) > 0:
            raise ValueError(f"An entry already exists for Event Id: {new_audit_obj.event_id}")
        
        self.db.add(new_audit_obj)
        self.db.flush()

        self.db.commit()
        self.db.refresh(new_audit_obj)

        return new_audit_obj