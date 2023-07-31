# Schemas (i.e. models) that will be used for the requests to the API
from pydantic import BaseModel
from datetime import datetime

# Create a Pending Update of the System Map Object
class CreateSystemMapUpdate(BaseModel):
    # create an entry in the staging table 
    hydraulic_system_name: str
    area_name: str | None = None
    region_name: str | None = None
    comments: str | None = None
    odmt_area_id: int | None = None
    
    def __repr__(self) -> str:
        return super().__repr__()
    
# create a pending update of the Sres entries
class CreateSresUpdate(BaseModel): 
    pass 

# create a pending update of the contact tanks entries
class CreateContactTanksUpdate(BaseModel): 
    pass
