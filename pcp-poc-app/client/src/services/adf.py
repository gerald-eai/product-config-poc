# use this to make requests to the ADF api
import requests
from services.api import BaseAPIClient
from schemas.adf_schemas import QueryPipelineRunsByFactory, TriggerPipelineRun, Pipeline, PipelineRun, PipelineRunByFactory
from typing import Optional, List
from datetime import datetime, timedelta


class DataFactoryAPIClient(BaseAPIClient):
    """_summary_

    ADF API Client for our application.
    Args:
        BaseAPIClient (_type_): _description_
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        super().__init__(base_url)
        print(f"{self.base_url}")

    def get_pipelines_list(self):
        """_summary_
        Get a list of pipelines in the application data factory.

        """
        response = self.get_request("/data-factory/pipelines")
        print(f"Response: {response}")
        if response.status_code == 200:
            json_response = response.json()
            pipeline_list = []
            for pl in json_response: 
                pipeline_list.append(Pipeline.parse_obj(pl))
            
            return pipeline_list
        else:
            raise ValueError(f"Error Getting the Pipelines in the Data Factory.")

    def get_pipeline(self, pipeline_name: str):
        """_summary_
        Gets information about the desired pipeline

        Args:
            pipeline_name (str): _description_
        """
        response = self.get_request(f"/data-factory/pipelines/{pipeline_name}")
        if response.status_code == 200:
            response_json = response.json()
            pipeline = Pipeline.parse_obj(response_json)
            
            return pipeline
        else:
            raise ValueError(
                f"Error Getting the Pipeline {pipeline_name} in the Data Factory."
            )

    def get_pipeline_run(self, run_id: str):
        response = self.get_request(f"/data-factory/pipelines/runs/{run_id}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error Getting Pipeline Run with id {run_id}")

    def trigger_pipeline_run(
        self, request_body: TriggerPipelineRun
    ):
        response = self.post_request(f"/data-factory/pipelines/runs/", data=request_body.dict())
        print(f"Response: {response.json()}")
        if response.status_code == 200:
            json_response = response.json()
            run_id = PipelineRun.parse_obj(json_response)
            return run_id
        else:
            raise ValueError(f"Error Triggering Pipeline {request_body.pipelineName}")

    def get_most_recent_pipeline_run(
        self,
        request_body: QueryPipelineRunsByFactory
        
    ) -> List[PipelineRunByFactory]:
        serialize_body = request_body.dict()
        response = self.post_request("/data-factory/pipelines/runs/most-recent", data=serialize_body)
        if response.status_code == 200: 
            # convert the response to the pydantic model 
            json_response = response.json() # list of pipeline run objects 
            pipeline_runs = []
            for run in json_response: 
                pipeline_runs.append(PipelineRunByFactory.parse_obj(run))
                
            return pipeline_runs
        else: 
            raise ValueError(f"Error Getting the Pipeline Runs for the Data Factory.")
