from sqlalchemy import Column, DateTime, Integer, String 
from db.database import Base 

class AuditLog(Base): 
    __tablename__ = "pcp_poc_audit_log"
    __table_args__={"schema": "DPSN_DEMO"}
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(String(10), nullable=False)
    table_altered=Column(String(50))
    event_type=Column(String(50))
    event_date=Column(DateTime)
    columns_altered=Column(String(1024))
    previous_value=Column(String(128))
    updated_value=Column(String(128))
    actor=Column(String(32))
    status=Column(String(24))
    pushed_to_live_date=Column(DateTime)
    row_altered=Column(String(50))
    
    def __repr__(self): 
        return f"AuditLogORM(id={self.id}, event_id={self.event_id}, table_altered={self.table_altered}, event_type={self.event_type}, event_date={self.event_date}, previous_value={self.previous_value}, updated_value={self.updated_value}, actor={self.actor})"
    