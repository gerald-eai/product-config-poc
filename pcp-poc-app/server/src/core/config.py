import os
from dotenv import load_dotenv
import os
from pydantic import Field
from pydantic import BaseSettings
from functools import lru_cache
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.keyvault.secrets import SecretClient
from typing import Optional

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env.local"))
app_env = os.environ.get("APP_ENVIRONMENT", "local")


class Settings(BaseSettings):
    APP_ENVIRONMENT: str = Field(env="APP_ENVIRONMENT")
    # local settings
    DB_HOSTNAME: str = Field(env="DB_HOSTNAME")
    DB_NAME: str = Field(env="DB_NAME")
    DB_USER: str = Field(env="DB_USER")
    DB_PWD: str = Field(env="DB_PWD")
    DB_PORT: str = Field(env="DB_PORT")
    DB_SCHEMA: str = Field(env="DB_SCHEMA")
    SQL_DRIVER: str = Field(env="SQL_DRIVER")

    # dev settings
    AZURE_TENANT_ID: str = Field(env="AZURE_TENANT_ID")
    AZURE_USERNAME: str = Field(env="AZURE_USERNAME")
    AZURE_PASSWORD: str = Field(env="AZURE_PASSWORD")
    AZURE_CLIENT_ID: str = Field(env="AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET: str = Field(env="AZURE_CLIENT_SECRET")
    AZURE_DATABASE: str = Field(env="AZURE_DATABASE")
    AZURE_HOSTNAME: str = Field(env="AZURE_HOSTNAME")
    AZURE_SCHEMA: str = Field(env="AZURE_SCHEMA")
    
    # ADF params 
    ADF_SUBSCRIPTION_ID: str = Field(env="ADF_SUBSCRIPTION_ID")
    ADF_RESOURCE_GROUP: str = Field(env="ADF_RESOURCE_GROUP")
    ADF_FACTORY_NAME: str = Field(env="ADF_FACTORY_NAME")

    # sn keyvault values
    SN_CLIENT_ID: Optional[str] = Field(env="SNServicePrincipleAppID")
    SN_CLIENT_SECRET: Optional[str] = Field(env="SNServicePrinciple")
    SN_HOSTNAME: Optional[str] = Field(env="DPlatSQLDB-HOST")
    SN_DATABASE: Optional[str] = Field(env="DPlatSQLDB-Database")

    class config:
        env_file = f".env.local"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @classmethod
    def load_from_sn_keyvault(cls):
        vault_uri = os.getenv("SN_KEY_VAULT_URI")
        credential = DefaultAzureCredential()
        vault_client = SecretClient(vault_url=vault_uri, credential=credential)
        secret_value = {}
        for field_name, field in cls.__fields__.items():
            field_info = field.field_info.extra.get("env")
            if field_info:
                if "SN_" in field_info:
                    secret_name = field.field_info.extra["env"]
                    secret = vault_client.get_secret(secret_name)
                    secret_value[field_name] = secret.value

        return cls(**secret_value)


@lru_cache(maxsize=10)
def get_settings():
    return Settings()


@lru_cache(maxsize=10)
def get_azure_keyvault_settings():
    return Settings.load_from_sn_keyvault()
