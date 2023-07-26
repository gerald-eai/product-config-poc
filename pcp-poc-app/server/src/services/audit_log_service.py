from sqlalchemy.orm import Session
from db.audit_log_repository import AuditLogRepository
from schemas.audit_log_schema import AuditLogDB
from api.requests.audit_log_requests import CreateAuditRequest
from core.utils.helper_functions import generate_audit_uuid


class AuditLogService:
    def __init__(self, db: Session):
        self.repository = AuditLogRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100):
        query = self.repository.get_all(skip, limit)
        return [AuditLogDB.from_db(el) for el in query]

    def get_by_event_id(self, event_id: str):
        query = self.repository.get_by_event_id(event_id)
        return AuditLogDB.from_db(query)

    def create_new_event(self, new_event: CreateAuditRequest):
        uuid_ = generate_audit_uuid()
        new_event.event_id = uuid_

        new_audit_entry = self.repository.create_event(new_event)

        return new_audit_entry
