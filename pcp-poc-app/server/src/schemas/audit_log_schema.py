from pydantic import BaseModel, ConfigDict
from datetime import datetime
from db.models.audit_log import AuditLog


# pydantic schema
class AuditLogBase(BaseModel):
    id: int
    event_id: str
    table_altered: str
    event_type: str
    event_date: datetime
    previous_value: str
    updated_value: str
    actor: str

    model_config = ConfigDict(from_attributes=True)


class AuditLogDB:
    id: int
    event_id: str
    table_altered: str
    event_type: str
    event_date: datetime
    previous_value: str
    updated_value: str
    actor: str

    def __init__(self, audit_log_db: AuditLog):
        print("inside the db object")
        self.id = audit_log_db.id
        self.event_id = audit_log_db.event_id
        self.table_altered = audit_log_db.table_altered
        self.event_date = audit_log_db.event_date
        self.event_type = audit_log_db.event_type
        self.previous_value = audit_log_db.previous_value
        self.updated_value = audit_log_db.updated_value
        self.actor = audit_log_db.actor
        print(self)

    def __repr__(self):
        return f"AuditLog(id={self.id}, \
            event_id={self.event_id}, table_altered={self.table_altered}, \
            event_date={self.event_date}, event_type={self.event_type}, previous_value={self.previous_value}, \
            updated_value={self.updated_value}, actor={self.actor})"

    @classmethod
    def from_db(cls, audit_log_db: AuditLog):
        return cls(audit_log_db)
