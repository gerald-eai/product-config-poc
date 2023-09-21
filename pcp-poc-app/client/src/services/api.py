import requests 
from typing import Any, Union
import schemas.request_models as request_models
from data.data_processor import convert_json_to_df

# have functions that will read from the API server 
class ApiConsumer(): 
    def __init__(self, base_url): 
        self.base_url = base_url
    
    def get_all(self, endpoint:str, params: request_models.RequestAll): 
        if params: 
            response = requests.get(self.base_url + endpoint, params=params)
        else: 
            response = requests.get(self.base_url+endpoint)
        return convert_json_to_df(response.json())
        
    
    def get_by_id(self, endpoint: str, params: Any):
        if params: 
            response = requests.get(self.base_url + endpoint + str(params))
        else: 
            response = requests.get(self.base_url + endpoint)
        return convert_json_to_df(response.json())
    
    def create_new_entry(self, endpoint: str, req_body: Any):
        # what are the entries that will be created 
        if req_body: 
            print(f"Request Body: {req_body.dict()}")
            response = requests.post(self.base_url + endpoint, json=req_body.dict())
            return convert_json_to_df([response.json()])
        else: 
            raise Exception("Request body is empty!")
    
    def create_staged_entry(self, endpoint: str, req_body: Any):
        if req_body: 
            print(f"Request Body: {req_body.dict()}")
            response = requests.post(self.base_url + endpoint, json=req_body.dict())
            return convert_json_to_df([response.json()])
        else: 
            raise Exception("Request body is empty!")
    
    def edit_entry(self, endpoint: str, req_body: Any):
        if req_body: 
            response = requests.put(self.base_url + endpoint, json=req_body.dict())
            return convert_json_to_df([response.json()])
        else: 
            raise Exception("Request body is empty!")
    
    def validate_response(response: requests.Response):
        if response.status_code==200: 
            return response.json()
        else: 
            raise response.raise_for_status()
    
    
def main(): 
    print("Main in the API consumer!")
    
    
if __name__ == "__main__": 
    main()
    