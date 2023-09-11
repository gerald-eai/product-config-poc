from sqlalchemy.orm import Session
from db.audit_log_repository import AuditLogRepository
from schemas.audit_log_schema import AuditLog 
from api.requests.audit_log_requests import CreateAuditRequest
from core.utils import generate_audit_uuid
from typing import List 

class AuditLogService:
    def __init__(self, db: Session):
        self.repository = AuditLogRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        query = self.repository.get_all(skip, limit)

        return query

    def get_by_event_id(self, event_id: str) -> AuditLog:
        query = self.repository.get_by_event_id(event_id)

        return query

    def create_new_event(self, new_event: CreateAuditRequest) -> AuditLog:
        uuid_ = generate_audit_uuid()
        new_event.event_id = uuid_

        new_audit_entry = self.repository.create_event(new_event)

        return new_audit_entry
