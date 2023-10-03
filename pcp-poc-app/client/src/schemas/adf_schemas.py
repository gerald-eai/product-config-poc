from pydantic import BaseModel
from datetime import datetime 
from typing import Optional 
from datetime import timedelta

class QueryPipelineRunsByFactory(BaseModel):
    pipelineName: str
    startDate: Optional[str] = (datetime.now() - timedelta(days=5)).isoformat()
    endDate: Optional[str] = datetime.now().isoformat()
    # optional params
    operator: Optional[str]
    operand: Optional[str]
    value: Optional[str]

class TriggerPipelineRun(BaseModel):
    pipelineName: str
    # query parameters
    isRecovery: Optional[bool]
    referencePipelineRunId: Optional[str]
    startActivityName: Optional[str]
    startFromFailure: Optional[bool]
    
class Pipeline(BaseModel): 
    id: Optional[str]
    name: Optional[str]
    type: Optional[str]
    properties: Optional[dict]
    etag: Optional[str]

class PipelineRun(BaseModel): 
    runId: str
    pipelineName: Optional[str]
    invokedBy: Optional[dict]
    runStart: Optional[str]
    runEnd: Optional[str]
    durationInMs: Optional[int]
    status: Optional[str]
    message: Optional[str]
    lastUpdated: Optional[str]
    annotations: Optional[list]
    
class PipelineRunByFactory(PipelineRun):
    id: Optional[str]
    debugRunId: Optional[str]
    runGroupId: Optional[str]
    pipelineReturnValue: Optional[str]
    runDimension: Optional[dict]
    isLatest: Optional[bool]

