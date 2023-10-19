# use this to make requests to the ADF api
from services.api import BaseAPIClient
from schemas.adf_schemas import (
    QueryPipelineRunsByFactory,
    TriggerPipelineRun,
    Pipeline,
    PipelineRun,
    PipelineRunByFactory,
)
from typing import List


class DataFactoryAPIClient(BaseAPIClient):
    """_summary_
    ADF API Client for our application.
    Runs all of the ADF API requests required.

    Args:
        BaseAPIClient (_type_): Base API Client Class
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        super().__init__(base_url)

    def get_pipelines_list(self) -> List[Pipeline]:
        """_summary_
        Gets the list of pipelines within the Data Factory.

        Raises:
            ValueError: An error occurs if the status code is not 200.

        Returns:
            List[Pipeline]: List of pipelines in the Data Factory.
        """
        response = self.get_request("/data-factory/pipelines")
        if response.status_code == 200:
            json_response = response.json()
            pipeline_list = []
            for pl in json_response:
                pipeline_list.append(Pipeline.parse_obj(pl))

            return pipeline_list
        else:
            raise ValueError(f"Error Getting the Pipelines in the Data Factory.")

    def get_pipeline(self, pipeline_name: str) -> Pipeline:
        """_summary_
        Gets the information for a specific Pipeline in the Data Factory.


        Args:
            pipeline_name (str): Pipeline of interest

        Raises:
            ValueError: return an error if the status code is not 200

        Returns:
            Pipeline: Pipeline information
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

    def get_pipeline_run(self, run_id: str) -> PipelineRunByFactory:
        """_summary_
        Gets the Pipeline Run information for a pipeline with a specific run id.

        Args:
            run_id (str): run id to get info from

        Raises:
            ValueError: Error if the status code is not 200

        Returns:
            PipelineRunByFactory: Pipeline Run information
        """
        response = self.get_request(f"/data-factory/pipelines/runs/{run_id}")
        if response.status_code == 200:
            response_json = response.json()
            pipeline_run = PipelineRunByFactory.parse_obj(response_json)
            return pipeline_run
        else:
            raise ValueError(f"Error Getting Pipeline Run with id {run_id}")

    def trigger_pipeline_run(self, request_body: TriggerPipelineRun) -> PipelineRun:
        """_summary_
        Triggers the ADF Pipeline Run to transform our Product Config tables.

        Args:
            request_body (TriggerPipelineRun): Request to trigger the pipeline

        Raises:
            ValueError: An error if status code returned is not OK

        Returns:
            PipelineRun: The Pipeline Run id is returned
        """
        response = self.post_request(
            f"/data-factory/pipelines/runs/", data=request_body.dict()
        )
        print(f"Response: {response.json()}")
        if response.status_code == 200:
            json_response = response.json()
            run_id = PipelineRun.parse_obj(json_response)
            return run_id
        else:
            raise ValueError(f"Error Triggering Pipeline {request_body.pipelineName}")

    def get_most_recent_pipeline_run(
        self, request_body: QueryPipelineRunsByFactory
    ) -> List[PipelineRunByFactory]:
        """_summary_
        Makes a request to get the most recent Pipeline Runs for a specific Pipeline name
        Args:
            request_body (QueryPipelineRunsByFactory): Contains the metadata required to make the request

        Raises:
            ValueError: Error if the code status is not 200

        Returns:
            List[PipelineRunByFactory]: list of Pipeline Runs in the Data Factory
        """
        serialize_body = request_body.dict()
        response = self.post_request(
            "/data-factory/pipelines/runs/most-recent", data=serialize_body
        )
        if response.status_code == 200:
            # convert the response to the pydantic model
            json_response = response.json()  # list of pipeline run objects
            pipeline_runs = []
            for run in json_response:
                pipeline_runs.append(PipelineRunByFactory.parse_obj(run))

            return pipeline_runs
        else:
            raise ValueError(f"Error Getting the Pipeline Runs for the Data Factory.")
