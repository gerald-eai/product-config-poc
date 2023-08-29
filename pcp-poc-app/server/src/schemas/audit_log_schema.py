from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional

class AuditLog(SQLModel, table=True): 
    __tablename__ = "pcp_poc_audit_log"
    __table_args__={"schema": "DPSN_DEMO"}
    id: int = Field(primary_key=True, index=True)
    event_id: str = Field(index=True)
    table_altered: str
    event_type: Optional[str] = Field(default=None)
    event_date: Optional[datetime] = Field(default=None)
    previous_value: Optional[str] = Field(default=None) 
    updated_value: Optional[str] = Field(default=None)
    actor: Optional[str] = Field(default=None)
    row_altered: Optional[str] = Field(default=None)
    columns_altered: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    pushed_to_live_date: Optional[datetime] = Field(default=None)
    
    def __repr__(self): 
        return f"AuditLogORM(id={self.id}, event_id={self.event_id}, table_altered={self.table_altered}, event_type={self.event_type}, event_date={self.event_date}, previous_value={self.previous_value}, updated_value={self.updated_value}, actor={self.actor})"
    