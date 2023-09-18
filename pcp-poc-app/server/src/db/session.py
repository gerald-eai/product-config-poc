from sqlalchemy.pool import QueuePool
from core.config import get_settings, get_azure_keyvault_settings
from core.auth import authenticate_client_key
from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy import event
import urllib
import pyodbc


# az_settings = get_azure_keyvault_settings()
settings = get_settings()

#
USER = settings.DB_USER
PWD = settings.DB_PWD
HOST = settings.DB_HOSTNAME
DB_NAME = settings.DB_NAME
PORT = settings.DB_PORT
SCHEMA = settings.DB_SCHEMA
SQL_DRIVER = settings.SQL_DRIVER
AZURE_TENANT_ID = settings.AZURE_TENANT_ID
AZURE_CLIENT_ID=settings.AZURE_CLIENT_ID
AZURE_CLIENT_SECRET=settings.AZURE_CLIENT_SECRET
AZURE_USERNAME = settings.AZURE_USERNAME
AZURE_PASSWORD = settings.AZURE_PASSWORD
AZURE_DATABASE = settings.AZURE_DATABASE
AZURE_HOSTNAME = settings.AZURE_HOSTNAME


# AZ_USER = az_settings.DB_USER
# AZ_PWD = az_settings.DB_PWD
# AZ_HOST = az_settings.DB_HOSTNAME
# AZ_DB_NAME = az_settings.DB_NAME
# AZ_PORT = az_settings.DB_PORT
# AZ_SCHEMA = az_settings.DB_SCHEMA
# AZ_SQL_DRIVER = az_settings.SQL_DRIVER
# AZ_CLIENT_ID = az_settings.SN_CLIENT_ID
# AZ_CLIENT_SECRET = az_settings.SN_CLIENT_SECRET
# AZ_TENANT_ID = az_settings.TENANT_ID

AAD_TOKEN = authenticate_client_key(
    tenant_id=AZURE_TENANT_ID,
    client_id=AZURE_CLIENT_ID,
    client_secret=AZURE_CLIENT_SECRET,
    resource_url="https://database.windows.net/",
)

print(f"ACCESS TOKEN: {AAD_TOKEN.token['access_token']}")
# connection string for LOCAL
driver_host_str = f"DRIVER={{{SQL_DRIVER}}};SERVER=tcp:{AZURE_HOSTNAME},{PORT};"
uid_str = f"DATABASE={AZURE_DATABASE};UID={AZURE_USERNAME};PWD={AZURE_PASSWORD};"
schema_str = f"CONNECTION TIMEOUT=60;SCHEMA={SCHEMA};Encrypt=yes;TrustServerCertificate=no;"
conn_str = urllib.parse.quote_plus(driver_host_str + uid_str + schema_str)

print(f"conn str: {conn_str}")

DB_URI = f"mssql+pyodbc:///?odbc_connect={conn_str}"
engine = create_engine(DB_URI, poolclass=QueuePool, pool_size=10, pool_pre_ping=True)


def get_session():
    try:
        db_session = Session(engine)
        yield db_session
    finally:
        db_session.close()
