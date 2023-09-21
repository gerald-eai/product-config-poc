from pydantic import BaseModel
from datetime import datetime


class BaseRequest(BaseModel):
    pass


class CreateNewLiveEntry(BaseRequest):
    pass


class CreateNewStagedEntry(BaseRequest):
    pass


class EditStagedEntry(BaseModel):
    pass
