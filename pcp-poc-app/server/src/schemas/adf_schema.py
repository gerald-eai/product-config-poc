from pydantic import BaseModel 
from typing import Optional, List
from datetime import datetime



class Pipeline(BaseModel): 
    id: Optional[str]
    name: Optional[str]
    type: Optional[str]
    properties: Optional[dict]
    etag: Optional[str]

# response model 
class CreatePipelineRun(BaseModel): 
    runId: str
    
class PipelineRun(BaseModel): 
    # used in the get request for Pipeline Runs
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
    # used when requesting by Factory for the pipelines
    id: Optional[str]
    debugRunId: Optional[str]
    runGroupId: Optional[str]
    pipelineReturnValue: Optional[str]
    runDimension: Optional[dict]
    isLatest: Optional[bool]
    