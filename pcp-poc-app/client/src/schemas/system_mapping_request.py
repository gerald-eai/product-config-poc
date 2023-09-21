# Model represents the request body for requests made to the system mapping APIs
from pydantic import BaseModel
from datetime import datetime


class CreateNewLiveEntry(BaseModel):
    # create a new live entry, everything except for Comments and last modified is required
    pass


class CreateNewStagedEntry(BaseModel):
    # create an entry in the staging table
    pass


class EditStagedEntry(BaseModel):
    # Edit an entry in the staged table
    pass
