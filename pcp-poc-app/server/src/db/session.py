from sqlalchemy.pool import QueuePool
from core.config import get_settings, get_azure_keyvault_settings
from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool
import urllib


# az_settings = get_azure_keyvault_settings()
settings = get_settings()

APP_ENV = settings.APP_ENVIRONMENT
# local config
LOCAL_USER = settings.DB_USER
LOCAL_PWD = settings.DB_PWD
LOCAL_HOST = settings.DB_HOSTNAME
LOCAL_DATABASE = settings.DB_NAME
LOCAL_SCHEMA = settings.DB_SCHEMA

# azure config
AZURE_USERNAME = settings.AZURE_USERNAME
AZURE_PASSWORD = settings.AZURE_PASSWORD
AZURE_DATABASE = settings.AZURE_DATABASE
AZURE_HOSTNAME = settings.AZURE_HOSTNAME
AZURE_SCHEMA = settings.AZURE_SCHEMA

PORT = settings.DB_PORT
SQL_DRIVER = settings.SQL_DRIVER

# connection strings '
driver_host_str = ""
uid_str = ""

if APP_ENV == "local":
    driver_host_str = f"DRIVER={{{SQL_DRIVER}}};SERVER=tcp:{LOCAL_HOST},{PORT};DATABASE={LOCAL_DATABASE};"
    uid_str = f"UID={LOCAL_USER};PWD={LOCAL_PWD};SCHEMA={LOCAL_SCHEMA};"
else:
    driver_host_str = f"DRIVER={{{SQL_DRIVER}}};SERVER=tcp:{AZURE_HOSTNAME},{PORT};DATABASE={AZURE_DATABASE};"
    uid_str = f"UID={AZURE_USERNAME};PWD={AZURE_PASSWORD};SCHEMA={AZURE_SCHEMA};"

schema_str = f"CONNECTION TIMEOUT=60;"
conn_str = driver_host_str + uid_str + schema_str
conn_str = urllib.parse.quote_plus(conn_str)

DB_URI = f"mssql+pyodbc:///?odbc_connect={conn_str}"
engine = create_engine(DB_URI, poolclass=QueuePool, pool_size=10, pool_pre_ping=True)


def get_session():
    try:
        db_session = Session(engine)
        yield db_session
    finally:
        db_session.close()
