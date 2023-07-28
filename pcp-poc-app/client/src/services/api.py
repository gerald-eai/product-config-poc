import requests 
from typing import Any, Union
import schemas.request_models as request_models
from data.data_processor import convert_json_to_df
# have functions that will read from the API server 
class ApiConsumer(): 
    def __init__(self, base_url): 
        self.base_url = base_url
    
    def get_all(self, endpoint:str, params: Union[request_models.RequestAll, None]=None): 
        if params: 
            response = requests.get(self.base_url + endpoint, params=params)
        else: 
            response = requests.get(self.base_url+endpoint)
        
        if response.status_code == 200: 
            return convert_json_to_df(response.json())
        else: 
            raise response.raise_for_status()
        
    
    def get_by_id(self, endpoint: str, params: Union[int, str, None]=None):
        if params: 
            response = requests.get(self.base_url + endpoint + str(params))
        else: 
            response = requests.get(self.base_url + endpoint)
        
        if response.status_code == 200: 
            return response.json()
        else: 
            raise response.raise_for_status()
    
    def create_new_entry(self, endpoint: str, params: Any):
        # what are the entries that will be created 
        pass 
    
    def update_existing_entry():
        pass 

def main(): 
    print("Main in the API consumer!")
    
    
if __name__ == "__main__": 
    main()
    