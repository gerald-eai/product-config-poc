from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class CreateAuditRequest(BaseModel):
    id: int | None = None
    event_id: str | None = None
    table_altered: str
    event_type: str
    event_date: datetime
    previous_value: str | None = None
    updated_value: str
    actor: str
    columns_altered: str 
    status: str 
    pushed_to_live_date: datetime | None = None
    row_altered: str
    
