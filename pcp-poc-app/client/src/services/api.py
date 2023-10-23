import requests
from typing import Any, Optional
import schemas.request_models as request_models
from data.data_processor import convert_json_to_df
from pandas import DataFrame


class BaseAPIClient:
    """_summary_

    This class is a wrapper for the API requests made to the FastAPI api endpoints.

    Args:
        BaseAPIClient (_type_): API Client Base Class

    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_request(
        self, endpoint: str, params: Optional[Any] = None
    ) -> Optional[requests.Response]:
        """_summary_
        Performs a get request to the api endpoint.

        Args:
            endpoint (str): endpoint url
            params (Optional[Any], optional): query parameters that are included in the url. Defaults to None.

        Returns:
            Optional[Response]: response from the url
        """
        url = self.base_url + endpoint
        if params:
            response = requests.get(url, params=params)
        else:
            response = requests.get(url)
        return response

    def post_request(
        self, endpoint: str, params: Optional[Any] = None, data: Optional[Any] = None
    ) -> Optional[requests.Response]:
        """_summary_
        Performs a post request to the api endpoint.

        Args:
            endpoint (str): endpoint url
            params (Optional[Any], optional): query parameters that are included in the url. Defaults to None.
            data (Optional[Any], optional): data that is included in the request body. Defaults to None.

        Returns:
            Optional[Response]: response from the url
        """

        url = self.base_url + endpoint
        if params and data:
            response = requests.post(url, params=params, json=data)
        else:
            response = requests.post(url, json=data)
        return response

    def put_request(
        self, endpoint: str, params: Optional[Any] = None, data: Optional[Any] = None
    ) -> Optional[requests.Response]:
        """_summary_
        Performs a put request to the api endpoint.

        Args:
            endpoint (str): endpoint url
            params (Optional[Any], optional): query parameters that are included in the url. Defaults to None.
            data (Optional[Any], optional): data that is included in the request body. Defaults to None.

        Returns:
            Optional[Response]: _description_
        """
        url = self.base_url + endpoint
        if params and data:
            response = requests.put(url, params=params, json=data)
        else:
            response = requests.put(url, json=data)
        return response


class DatabaseAPIClient(BaseAPIClient):
    """_summary_

    This class is a wrapper for the API requests made to the database api endpoints.

    Args:
        BaseAPIClient (_type_): API Client Base Class
    """

    def __init__(self, base_url: str):
        super().__init__(base_url)

    def get_all(self, endpoint: str, params: request_models.RequestAll) -> DataFrame:
        """_summary_
        Returns paginated data from the database.

        Args:
            endpoint (str): DB endpoint url
            params (request_models.RequestAll): request params

        Returns:
            DataFrame: the table data in the form of a dataframe
        """
        if params:
            response = self.get_request(endpoint, params=params)
        else:
            response = self.get_request(endpoint)

        return convert_json_to_df(response.json())

    def get_by_id(self, endpoint: str, params: Any) -> DataFrame:
        """_summary_
        Returns data from the database by id.

        Args:
            endpoint (str): DB endpoint url
            params (Any): request params

        Returns:
            _type_: The data from the database
        """
        if params:
            response = self.get_request(endpoint + str(params))
        else:
            response = self.get_request(endpoint)
        return convert_json_to_df(response.json())

    def create_new_entry(self, endpoint: str, req_body: Any) -> DataFrame:
        """_summary_
        Create a new entry in the database

        Args:
            endpoint (str): url for the desired table
            req_body (Any): New entry added to the table

        Raises:
            ValueError: Error if no new entry data is provided

        Returns:
            DataFrame: New database entry
        """
        if req_body:
            response = self.post_request(endpoint, data=req_body.dict())
            return convert_json_to_df([response.json()])
        else:
            raise ValueError("Cannot create a new entry try again.")

    def edit_entry(self, endpoint: str, req_body: Any) -> DataFrame:
        """_summary_

        Args:
            endpoint (str): url for the desired table
            req_body (Any): Edited data for the table

        Raises:
            ValueError: Error if no data is provided

        Returns:
            DataFrame: Updated database entry
        """
        if req_body:
            response = self.put_request(endpoint, data=req_body.dict())
            return convert_json_to_df([response.json()])
        else:
            raise ValueError("Cannot edit, try again.")

    def validate_response(response: requests.Response):
        if response.status_code == 200:
            return response.json()
        else:
            raise response.raise_for_status()
