from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class CreateAuditRequest(BaseModel):
    id: Optional[int]
    event_id: Optional[str]
    table_altered: str
    event_type: str
    event_date: datetime
    previous_value: Optional[str]
    updated_value: str
    actor: str
    columns_altered: str 
    status: str 
    pushed_to_live_date: Optional[datetime]
    row_altered: str
    
