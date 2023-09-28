from pydantic import BaseModel
from typing import List, Optional 


class TriggerPipelineRequest(BaseModel):
    # query parameters
    isRecovery: Optional[bool]
    referencePipelineRunId: Optional[str]
    startActivityName: Optional[str]
    startFromFailure: Optional[bool]