from datetime import datetime

from pydantic import BaseModel


class CreateAuditRequest(BaseModel):
    id: int | None = None
    event_id: str | None = None
    table_altered: str
    event_type: str
    event_date: datetime
    previous_value: str | None = None
    updated_value: str
    actor: str
