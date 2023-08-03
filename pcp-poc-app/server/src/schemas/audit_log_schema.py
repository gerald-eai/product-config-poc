from pydantic import BaseModel, ConfigDict
from datetime import datetime
from db.models.audit_log import AuditLog


# pydantic schema
class AuditLogBase(BaseModel):
    id: int
    event_id: str
    table_altered: str
    event_type: str 
    event_date: datetime | None = None 
    previous_value: str | None = None 
    updated_value: str | None = None 
    actor: str | None = None 
    row_altered: str | None = None 
    columns_altered: str | None = None 
    status: str | None = None 
    pushed_to_live_date: datetime | None = None 

    model_config = ConfigDict(from_attributes=True)


class AuditLogDB:
    id: int
    event_id: str
    table_altered: str
    event_type: str | None = None 
    event_date: datetime | None = None 
    previous_value: str | None = None 
    updated_value: str | None = None 
    actor: str | None = None 
    row_altered: str | None = None 
    columns_altered: str | None = None 
    status: str | None = None 
    pushed_to_live_date: datetime | None = None 

    def __init__(self, audit_log_db: AuditLog):
        self.id = audit_log_db.id
        self.event_id = audit_log_db.event_id
        self.table_altered = audit_log_db.table_altered
        self.event_date = audit_log_db.event_date
        self.event_type = audit_log_db.event_type
        self.previous_value = audit_log_db.previous_value
        self.updated_value = audit_log_db.updated_value
        self.actor = audit_log_db.actor
        self.columns_altered = audit_log_db.columns_altered
        self.row_altered = audit_log_db.row_altered
        self.status = audit_log_db.status
        self.pushed_to_live_date = audit_log_db.pushed_to_live_date

    def __repr__(self):
        return f"AuditLog(id={self.id}, \
            event_id={self.event_id}, table_altered={self.table_altered}, \
            event_date={self.event_date}, event_type={self.event_type}, previous_value={self.previous_value}, \
            updated_value={self.updated_value}, actor={self.actor})"

    @classmethod
    def from_db(cls, audit_log_db: AuditLog):
        return cls(audit_log_db)
