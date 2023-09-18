from msal import ConfidentialClientApplication
from msrestazure.azure_active_directory import AADTokenCredentials
from .config import get_azure_keyvault_settings


def authenticate_client_key(
    tenant_id: str,
    client_id: str,
    client_secret: str,
    resource_url: str = "https://database.windows.net/",
) -> AADTokenCredentials:
    authority_host_uri = "https://login.microsoftonline.com"
    authority_uri = authority_host_uri + "/" + tenant_id

    app = ConfidentialClientApplication(
        client_id, authority=authority_uri, client_credential=client_secret
    )
 
    token_response = app.acquire_token_for_client(scopes=[resource_url + "/.default"])
    credentials = AADTokenCredentials(token_response, client_id)
    return credentials

def get_cached_token():
    pass