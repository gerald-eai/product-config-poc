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
    row_id_altered: str
    
