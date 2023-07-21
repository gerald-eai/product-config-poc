import os 
from dotenv import load_dotenv
import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


# load the data from our .env file
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                         ".env.dev"))

class Settings(BaseSettings):
    AZ_DB_HOSTNAME: str = Field(env="AZ_DB_HOSTNAME")
    AZ_DB_NAME: str = Field(env="AZ_DB_NAME")
    AZ_DB_USER: str=Field(env="AZ_DB_USER")
    AZ_DB_PWD: str = Field(env="AZ_DB_PWD")
    AZ_DB_PORT: str=Field(env="AZ_DB_PORT")
    AZ_DB_SCHEMA: str=Field(env="AZ_DB_SCHEMA")
    
    model_config=SettingsConfigDict(env_file=".env.dev")

@lru_cache(maxsize=10)
def get_settings():
    return Settings()


