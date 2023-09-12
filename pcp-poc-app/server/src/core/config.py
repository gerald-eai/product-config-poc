import os
from dotenv import load_dotenv
import os
from pydantic import Field

# from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseSettings
from functools import lru_cache
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app_env = os.environ.get("APP_ENVIRONMENT", "local")
if app_env == "local":
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env.local"))
else:
    # load the data from our .env file
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env.dev"))
print(app_env)


class Settings(BaseSettings):
    DB_HOSTNAME: str = Field(env="DB_HOSTNAME")
    DB_NAME: str = Field(env="DB_NAME")
    DB_USER: str = Field(env="DB_USER")
    DB_PWD: str = Field(env="DB_PWD")
    DB_PORT: str = Field(env="DB_PORT")
    DB_SCHEMA: str = Field(env="DB_SCHEMA")
    SQL_DRIVER: str = Field(env="SQL_DRIVER")

    class config:
        env_file = f".env.{os.getenv('APP_ENVIRONMENT', f'{app_env}')}"
        env_file_encoding = "utf-8"
        case_sensitive = True


class AzureKeyVaultSettings(BaseSettings):
    # SN Settings
    SN_CLIENT_ID: str = Field(env="SNServicePrincipleAppID")
    SN_CLIENT_SECRET: str = Field(env="SNServicePrinciple")
    DB_HOSTNAME: str = Field(env="DPlatSQLDB-HOST")
    DB_NAME: str = Field(env="DPlatSQLDB-Database")
    DB_USER: str = Field(env="z-one-username")
    DB_PWD: str = Field(env="z-one-password")

    # Regular DB settings
    DB_SCHEMA: str = Field(env="DB_SCHEMA")
    SQL_DRIVER: str = Field(env="SQL_DRIVER")
    DB_PORT: str = Field(env="DB_PORT")
    TENANT_ID: str = Field(env="TENANT_ID")

    @classmethod
    def load_from_sn_keyvault(cls):
        vault_uri = os.getenv("SN_KEY_VAULT_URI")
        credential = DefaultAzureCredential()
        vault_client = SecretClient(vault_url=vault_uri, credential=credential)
        secret_value = {}
        for field_name, field in cls.__fields__.items():
            field_info = field.field_info.extra.get("env")
            if field_info:
                if (
                    field_info == "DB_SCHEMA"
                    or field_info == "SQL_DRIVER"
                    or field_info == "TENANT_ID"
                    or field_info == "DB_PORT"
                ):
                    continue
                else:
                    secret_name = field.field_info.extra["env"]
                    secret = vault_client.get_secret(secret_name)
                    secret_value[field_name] = secret.value

        return cls(**secret_value)


@lru_cache(maxsize=10)
def get_settings():
    return Settings()


@lru_cache(maxsize=10)
def get_azure_keyvault_settings():
    return AzureKeyVaultSettings.load_from_sn_keyvault()
