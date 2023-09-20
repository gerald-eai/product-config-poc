from msal import ConfidentialClientApplication
from msrestazure.azure_active_directory import AADTokenCredentials
from .config import get_settings
from cachetools import TTLCache

# loading settings, and getting all of our env variables
settings = get_settings()
cache = TTLCache(maxsize=1, ttl=3600)
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
    token = cache.get("aad_token")
    if token is None:
        result = msal_app.acquire_token_for_client(
            scopes=["https://database.windows.net/.default"],
        )
        if "access_token" in result.keys():
            token = result["access_token"]
            cache["aad_token"] = token
    return token

