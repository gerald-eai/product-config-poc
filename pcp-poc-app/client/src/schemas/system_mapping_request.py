# Model represents the request body for requests made to the system mapping APIs 
from pydantic import BaseModel 
from datetime import datetime

class CreateNewLiveEntry(BaseModel): 
    # create a new live entry, everything except for Comments and last modified is required
    hydraulic_system_name: str # it is a primary key but we define it
    area_name: str 
    region_name: str 
    comments: str | None = None
    odmt_area_id: int
    last_modified: datetime | None = None

class CreateNewStagedUpdate(BaseModel): 
     # create an entry in the staging table
    hydraulic_system_name: str
    area_name: str 
    region_name: str 
    comments: str | None = None
    odmt_area_id: int 
    updated_date: datetime | None = None
    def __repr__(self) -> str:
        return super().__repr__()

class EditStagedUpdate(BaseModel): 
    # Edit an entry in the staged table
    id: int 
    hydraulic_system_name: str
    area_name: str | None = None 
    region_name: str | None = None
    comments: str | None = None
    odmt_area_id: int | None = None
    updated_date: datetime | None = None
    
