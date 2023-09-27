# Use this as a means to connect to the ADF pipelines
# create the api request functions required to connect to the ADF pipelines
from core.config import get_settings
from core.auth import get_cached_token, get_user_impersonation_token
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.identity import DefaultAzureCredential
import requests
import json
from typing import Optional, List, Dict, Annotated

# pipeline run APIs 
class DataFactoryService:
    # our class responsible for all of the API calls to the Data Factory          
    def __init__(self, azure_credentials: DefaultAzureCredential): 
        self.subscription_id, self.resource_group_name, self.factory_name = self._get_adf_settings()
        self.client = self._create_adf_client(azure_credentials, self.subscription_id)
        self.adf_base_uri = self._create_adf_uri(self.resource_group_name, self.factory_name, self.subscription_id)
    
    @staticmethod
    def _create_adf_client(credentials, subscription_id) -> DataFactoryManagementClient:
        adf_client = DataFactoryManagementClient(credential=credentials, subscription_id=subscription_id)
        return adf_client 
    
    @staticmethod
    def _create_adf_uri(resource_group_name, factory_name, subscription_id): 
        return f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.DataFactory/factories/{factory_name}"
    
    @staticmethod
    def _get_adf_settings(): 
        settings = get_settings()
        return settings.ADF_SUBSCRIPTION_ID, settings.ADF_RESOURCE_GROUP, settings.ADF_FACTORY_NAME
    
    @staticmethod
    def _get_aad_token(): 
        # token = get_cached_token()
        token = get_user_impersonation_token()
        return token
    
    def list_by_factory(self): 
        """ 
        list the pipelines found in the ADF 
        """
        print(f"Listing by the Factory Name")
        pipelines = self.client.pipelines.list_by_factory(self.resource_group_name, self.factory_name)
        if pipelines is None: 
            raise ValueError("No Pipelines returned. Perhaps the factory name is incorrect!")
        return pipelines
    
    def get_pipeline(self, pipeline_name: str):
        """ 
        Get Pipeline infor based on the pipeline_name
        """ 
        
        adf_uri = self.adf_base_uri + f"/pipelines/{pipeline_name}?api-version=2018-06-01"
        print(f"ADF URI: {adf_uri}")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self._get_aad_token()
        }
        response = requests.get(adf_uri, headers=headers)
        if response.status_code == 200: 
            pipeline_info = response.json()
            return pipeline_info
        else: 
            print(f"Response: {response.json()['error']}")
            raise ValueError("No Pipelines returned. Perhaps the factory name is incorrect!")
        
        # pipeline_info = self.client.pipelines.get(self.resource_group_name, self.factory_name, pipeline_name=pipeline_name)
        # return pipeline_info 
    
    def get_job_ids(self): 
        pass 
    
    def create_job_run(self): 
        pass
    
    
    
    
    
    
    
