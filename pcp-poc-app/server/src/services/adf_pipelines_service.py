# Use this as a means to connect to the ADF pipelines
# create the api request functions required to connect to the ADF pipelines
import json
from datetime import datetime, timedelta
from typing import List, Optional

import requests
import schemas.adf_schema as DataFactory
from api.requests.adf_requests import TriggerPipelineRequest
from azure.identity import DefaultAzureCredential
from core.auth import get_user_impersonation_token
from core.config import get_settings


# pipeline run APIs
class DataFactoryService:
    # our class responsible for all of the API calls to the Data Factory
    def __init__(self, azure_credentials: DefaultAzureCredential):
        (
            self.subscription_id,
            self.resource_group_name,
            self.factory_name,
        ) = self._get_adf_settings()
        self.adf_base_uri = self._create_adf_uri(
            self.resource_group_name, self.factory_name, self.subscription_id
        )

    @staticmethod
    def _create_adf_uri(resource_group_name, factory_name, subscription_id):
        return f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.DataFactory/factories/{factory_name}"

    @staticmethod
    def _get_adf_settings():
        settings = get_settings()
        return (
            settings.ADF_SUBSCRIPTION_ID,
            settings.ADF_RESOURCE_GROUP,
            settings.ADF_FACTORY_NAME,
        )

    @staticmethod
    def _get_aad_token():
        # token = get_cached_token()
        token = get_user_impersonation_token()
        return token

    def list_by_factory(self) -> List[DataFactory.Pipeline]:
        """
        list the pipelines found in the ADF
        Use the requests api instead of the client sdk
        """
        adf_uri = self.adf_base_uri + f"/pipelines?api-version=2018-06-01"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self._get_aad_token(),
        }
        response = requests.get(adf_uri, headers=headers)
        if response.status_code == 200:
            pipeline_response = response.json()

            pipelines_list = []
            for item in pipeline_response["value"]:
                pipelines_list.append(DataFactory.Pipeline.parse_obj(item))

            return pipelines_list
        else:
            raise ValueError(f"Error Getting the pipelines.")

    def get_pipeline(self, pipeline_name: str) -> DataFactory.Pipeline:
        """
        Get Pipeline info based on the pipeline_name
        """

        adf_uri = (
            self.adf_base_uri + f"/pipelines/{pipeline_name}?api-version=2018-06-01"
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self._get_aad_token(),
        }
        response = requests.get(adf_uri, headers=headers)
        if response.status_code == 200:
            pipeline_info = response.json()
            pipeline_info = DataFactory.Pipeline.parse_obj(pipeline_info)
            return pipeline_info
        else:
            raise ValueError("No Pipelines returned!")

    def get_pipeline_run(self, run_id: str) -> DataFactory.PipelineRun:
        """_summary_
        Use ADF API to get the run information for a pipeline run.
        Args:
            run_id (str): Run ID to get context for

        Raises:
            ValueError: Error based on not finding pipeline run information

        Returns:
            Run info for a specific run id of a pipeline.
        """
        adf_uri = self.adf_base_uri + f"/pipelineruns/{run_id}?api-version=2018-06-01"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self._get_aad_token(),
        }
        response = requests.get(adf_uri, headers=headers)
        if response.status_code == 200:
            pipeline_info = response.json()
            pipeline_run = DataFactory.PipelineRun.parse_obj(pipeline_info)

            return pipeline_run
        else:
            raise ValueError(f"Error Getting the pipelines.")

    def create_job_run(
        self, pipeline_name: str, query_params: Optional[TriggerPipelineRequest]
    ) -> DataFactory.CreatePipelineRun:
        """_summary_
        Post request to create a job run for a specific pipeline.
        returns the job id.

        Args:
            query_params (Optional[TriggerPipelineRequest]):
                Optional query parameters for the POST request of the applicaiton

        Returns: pipeline_run information
            _type_: _description_
        """
        adf_uri = (
            self.adf_base_uri
            + f"/pipelines/{pipeline_name}/createRun?api-version=2018-06-01"
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self._get_aad_token(),
        }
        response = requests.post(adf_uri, headers=headers)
        if response.status_code == 200:
            pipeline_run = response.json()
            pipeline_run_id = DataFactory.CreatePipelineRun.parse_obj(
                pipeline_run["value"]
            )

            return pipeline_run_id
        else:
            raise ValueError(f"Error Triggering the Pipeline!")

    def most_recent_runs(
        self,
        pipeline_name: str,
        start_date: datetime = datetime.now() - timedelta(days=1),
        end_date: datetime = datetime.now(),
    ) -> List[DataFactory.PipelineRunByFactory]:
        """_summary_
        Get the pipeline runs for a specific pipeline.

        Args:
            pipeline_name (str): Pipeline name to get the pipeline runs for
            start_date (Optional[datetime], optional): Start date for the pipeline runs. Defaults to datetime.now().
            end_date (Optional[datetime], optional): End date for the pipeline runs. Defaults to timedelta(days=-1).

        Raises:
            ValueError: Error based on failed request

        Returns:
            List of pipeline runs for a specific pipeline.
        """

        adf_uri = self.adf_base_uri + f"/queryPipelineRuns?api-version=2018-06-01"

        filters = {
            "lastUpdatedAfter": f"{start_date}",
            "lastUpdatedBefore": f"{end_date}",
            "filters": [
                {
                    "operand": "PipelineName",
                    "operator": "Equals",
                    "values": [f"{pipeline_name}"],
                }
            ],
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self._get_aad_token(),
        }
        response = requests.post(adf_uri, headers=headers, data=json.dumps(filters))
        if response.status_code == 200:
            response_json = response.json()
            pipeline_runs = []
            for item in response_json["value"]:
                pipeline_runs.append(DataFactory.PipelineRun.parse_obj(item))
            return pipeline_runs

        else:
            raise ValueError(f"Error Getting the pipeline runs.")

    def get_job_run_by_status(self, pipelie_name: str):
        pass
