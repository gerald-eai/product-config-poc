from msal import ConfidentialClientApplication
from msrestazure.azure_active_directory import AADTokenCredentials
from azure.identity import (
    DefaultAzureCredential,
    InteractiveBrowserCredential,
)
from .config import get_settings
from cachetools import TTLCache

# loading settings, and getting all of our env variables
settings = get_settings()
cache = TTLCache(maxsize=10, ttl=3600)
msal_app = ConfidentialClientApplication(
    client_id=settings.AZURE_CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}",
    client_credential=settings.AZURE_CLIENT_SECRET,
)


def authenticate_client_key(
    tenant_id: str,
    client_id: str,
    client_secret: str,
    resource_url: str = "https://database.windows.net/",
) -> AADTokenCredentials:
    """Using the tenant id, client id, and client secret, this app generates 
        the AAD token credentials required to connect to the Azure sql server 
        that is holding configuration data for the API server.

    Args:
        tenant_id (str): Azure subscription tenant id
        client_id (str): Azure client id
        client_secret (str): Azure client secret
        resource_url (str, optional): Azure resource url. Defaults to "https://database.windows.net/".

    Returns:
        AADTokenCredentials: AAD credentials for the API.
    """
    # we want to get the AAD token, but only if it
    authority_host_uri = "https://login.microsoftonline.com"
    authority_uri = authority_host_uri + "/" + tenant_id

    app = ConfidentialClientApplication(
        client_id, authority=authority_uri, client_credential=client_secret
    )

    token_response = app.acquire_token_for_client(scopes=[resource_url + "/.default"])
    credentials = AADTokenCredentials(token_response, client_id)
    return credentials


def get_cached_token():
    """Gets access token for database authentication.
        Primarly used when connecting to the SQL server database.
        Cached by the application.

    Returns:
        str: AAD access token
    """
    token = cache.get("aad_token")
    if token is None:
        result = msal_app.acquire_token_for_client(
            scopes=["https://management.azure.com/.default"],
        )
        if "access_token" in result.keys():
            token = result["access_token"]
            cache["aad_token"] = token
    return token


def get_azure_credentials():
    credentials = cache.get("adf_credentials")
    if credentials is None:
        credentials = DefaultAzureCredential()
        # credentials = ClientSecretCredential(client_id=settings.AZURE_CLIENT_ID, client_secret=settings.AZURE_CLIENT_SECRET, tenant_id=settings.AZURE_TENANT_ID)
        cache["adf_credentials"] = credentials

    return credentials


def get_user_impersonation_token():
    """Authenticates the user using the InteractiveBrowserCredential, generates an access token
        which is then cached and used across the API. 
        Uses Interactive Browser Credential to get Azure credentials. 

    Returns:
        str: The AAD access token
    """
    access_token = cache.get("user_impersonation_token")
    if access_token is None:
        try:
            credential = InteractiveBrowserCredential()
            token_ = credential.get_token("https://management.azure.com/.default")
            access_token = token_.token
            cache["user_impersonation_token"] = access_token
            # return access_token
        except Exception as e:
            print(f"Auth Failed: {e}")
    return access_token
