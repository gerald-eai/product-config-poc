# Repository for the Audit log
from sqlalchemy.orm import Session
from db.models.audit_log import AuditLog
from api.requests.audit_log_requests import CreateAuditRequest


class AuditLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return (
            self.db.query(AuditLog)
            .order_by(AuditLog.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_event_id(self, event_id: str):
        return self.db.query(AuditLog).filter(AuditLog.event_id == event_id).first()

    def create_event(self, new_log: CreateAuditRequest):
        # create a new entry with data provided
        new_audit_obj = AuditLog(**new_log.model_dump())
        self.db.add(new_audit_obj)
        self.db.flush()

        self.db.commit()
        self.db.refresh(new_audit_obj)

        return new_audit_obj
