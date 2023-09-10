import os 
from dotenv import load_dotenv
import os
from pydantic import Field
# from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseSettings
from functools import lru_cache

app_env = os.environ.get("APP_ENVIRONMENT", "local")
if app_env == "local": 
    print("load local")
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                         ".env.local"))
else: 
    # load the data from our .env file
    print("load dev")
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                            ".env.dev"))
print(app_env)
class Settings(BaseSettings):
    AZ_DB_HOSTNAME: str = Field(env="AZ_DB_HOSTNAME")
    AZ_DB_NAME: str = Field(env="AZ_DB_NAME")
    AZ_DB_USER: str=Field(env="AZ_DB_USER")
    AZ_DB_PWD: str = Field(env="AZ_DB_PWD")
    AZ_DB_PORT: str=Field(env="AZ_DB_PORT")
    AZ_DB_SCHEMA: str=Field(env="AZ_DB_SCHEMA")
    SQL_DRIVER: str=Field(env="SQL_DRIVER")
    
    class config:
        env_file = f".env.{os.getenv('APP_ENVIRONMENT', f'{app_env}')}"
        env_file_encoding = 'utf-8'
        case_sensitive = True

@lru_cache(maxsize=10)
def get_settings():
    return Settings()


