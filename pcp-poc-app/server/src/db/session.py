from sqlalchemy.pool import QueuePool
from core.config import get_settings
from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool 
from sqlalchemy import event
import urllib
import pyodbc



settings = get_settings()
USER = settings.AZ_DB_USER
PWD = settings.AZ_DB_PWD
HOST = settings.AZ_DB_HOSTNAME
DB_NAME = settings.AZ_DB_NAME
PORT = settings.AZ_DB_PORT
SCHEMA = settings.AZ_DB_SCHEMA
SQL_DRIVER = settings.SQL_DRIVER

# connection string for LOCAL 
driver_host_str = f"DRIVER={{{SQL_DRIVER}}};SERVER={HOST},{PORT};"
uid_str = f"DATABASE={DB_NAME};UID={USER};PWD={PWD};"
schema_str = f"CONNECTION TIMEOUT=60;SCHEMA={SCHEMA};"
conn_str = driver_host_str + uid_str + schema_str

# two different DB_URIs, 1 for local development and another for deployed development

# conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=tcp:sqls-euw-dev-dplatsql.database.windows.net;"\
#                 f"DATABASE={DB_NAME};UID={USER};PWD={PWD};"\
#                 f"ENCRYPT=yes;TRUSTSERVERCERTIFICATE=no;CONNECTION TIMEOUT=30;"\
#                 f"AUTHENTICATION=ActiveDirectoryPassword"

# conn_str = urllib.parse.quote_plus(f"Driver={{ODBC Driver 17 for SQL Server}};Server={HOST},{PORT};DATABASE={DB_NAME};UID={USER};PWD={PWD};Authentication=ActiveDirectoryPassword")


DB_URI = f"mssql+pyodbc:///?odbc_connect={conn_str}"

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
