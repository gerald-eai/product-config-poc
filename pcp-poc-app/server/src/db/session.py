from sqlalchemy.pool import QueuePool
from core.config.config import get_settings
from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool 


settings = get_settings()
USER = settings.AZ_DB_USER
PWD = settings.AZ_DB_PWD
HOST = settings.AZ_DB_HOSTNAME
DB_NAME = settings.AZ_DB_NAME
PORT = settings.AZ_DB_PORT
SCHEMA = settings.AZ_DB_SCHEMA

# connection string
driver_host_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER=localhost,1433;"
uid_str = "DATABASE=PCP_POC_DB;UID=sa;PWD=L0ckedUp;"
schema_str = f"CONNECTION TIMEOUT=60;SCHEMA=DPSN_DEMO;"
connection_string = driver_host_str + uid_str + schema_str

# two different DB_URIs, 1 for local development and another for deployed development
DB_URI = f"mssql+pyodbc:///?odbc_connect={connection_string}"

engine = create_engine(
    DB_URI,
    poolclass=QueuePool,
    pool_size=20,
    pool_pre_ping=True
)


def get_session():
    try:
        db_session = Session(engine)
        yield db_session
    finally:
        db_session.close()
