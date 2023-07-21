from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys 
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from core.config import config as config_manager
import pyodbc, struct
from urllib.parse import quote_plus
from azure import identity

print([x for x in pyodbc.drivers()])
settings = config_manager.get_settings()
USER = settings.AZ_DB_USER
PWD = settings.AZ_DB_PWD
HOST = settings.AZ_DB_HOSTNAME
DB_NAME = settings.AZ_DB_NAME
PORT = settings.AZ_DB_PORT
SCHEMA = settings.AZ_DB_SCHEMA

# connection string
driver_host_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=localhost,1433;"
uid_str = "DATABASE=PCP_POC_DB;UID=sa;PWD=L0ckedUp;"
schema_str =  f"CONNECTION TIMEOUT=60;SCHEMA=DPSN_DEMO;"
connection_string = driver_host_str + uid_str + schema_str

# interactive authentication 
# connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={HOST},1433;DATABASE={DB_NAME};UID={USER};ENCRYPT=yes;TrustServerCertificate=no;CONNECTION TIMEOUT=60;Authentication=ActiveDirectoryIntegrated"

# two different DB_URIs, 1 for local development and another for deployed development
DB_URI = f"mssql+pyodbc:///?odbc_connect={connection_string}"

db_uri_local = f"mssql+pyodbc://?SA:L0ckedUp@localhost:1433/PCP_POC_DB"

# create engine to run 
engine = create_engine(DB_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    try: 
        
        db = SessionLocal()
        yield db 
    finally: 
        db.close()

# try: 
#     conn = engine.connect()
#     print("Database Connected")
#     conn.close()
# except Exception as e: 
#     print(f"Connection Failed: \n{e}") 