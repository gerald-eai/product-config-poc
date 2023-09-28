from pydantic import BaseModel
from typing import List, Optional 
from datetime import datetime, timedelta




class TriggerPipelineRequest(BaseModel):
    # query parameters
    isRecovery: Optional[bool]
    referencePipelineRunId: Optional[str]
    startActivityName: Optional[str]
    startFromFailure: Optional[bool]
    
class PipelineRunFiltersRequest(BaseModel): 
    # provide optional parameters here
    pipelineName: str
    startDate: Optional[datetime] = datetime.now() - timedelta(days=1)
    endDate: Optional[datetime] = datetime.now()

    operator: Optional[str]
    operand: Optional[str]
    value: Optional[str]