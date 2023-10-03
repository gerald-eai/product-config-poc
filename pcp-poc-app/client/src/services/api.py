import requests 
from typing import Any, Optional
import schemas.request_models as request_models
from data.data_processor import convert_json_to_df


class BaseAPIClient: 
    def __init__(self, base_url: str): 
        self.base_url = base_url
    
    def get_request(self, endpoint:str, params:Optional[Any] = None): 
        url = self.base_url + endpoint
        if params: 
            response = requests.get(url, params=params)
        else: 
            response=requests.get(url)
        return response
    
    def post_request(self, endpoint:str, params:Optional[Any] = None, data: Optional[Any]=None): 
        url = self.base_url + endpoint
        print(f"POST URL: {url}")
        if params and data: 
            response = requests.post(url, params=params, json=data)
        else: 
            response = requests.post(url, json=data)
        return response
    
class DatabaseAPIClient(BaseAPIClient):
    """_summary_
    
    This class is a wrapper for the API requests made to the database api endpoints.
    
    Args:
        BaseAPIClient (_type_): API Client Base Class
    """
    def __init__(self, base_url: str): 
        super().__init__(base_url)
        
    def get_all(self, endpoint:str, params: request_models.RequestAll): 
        if params: 
            response = self.get_request(endpoint, params=params)
        else: 
            response = self.get_request(endpoint)
            
        return convert_json_to_df(response.json())
    
    def get_by_id(self, endpoint:str, params:Any): 
        if params: 
            response = self.get_request(endpoint + str(params))
        else: 
            response = self.get_request(endpoint)
        return convert_json_to_df(response.json())
    
    def create_new_entry(self, endpoint:str, req_body:Any):
        if req_body: 
            response = self.post_request(endpoint, data=req_body.dict())
            return convert_json_to_df([response.json()])
        else: 
            raise ValueError("Request body cannot be empty! New entry not created.")
    
    def edit_entry(self, endpoint:str, req_body:Any): 
        if req_body: 
            response = self.post_request(endpoint, data=req_body.dict())
            return convert_json_to_df([response.json()])
        else: 
            raise ValueError("Request body cannot be empty! No edits made.")

    def validate_response(response: requests.Response):
        if response.status_code==200: 
            return response.json()
        else: 
            raise response.raise_for_status()
    
def main(): 
    print("Main in the API consumer!")
    
    
if __name__ == "__main__": 
    main()
    