# FastAPI Server

The FastAPI Server serves as the backend for handling API requests from the Product Configuration Portal POC.

## Steps to Run the API Server 
### Prerequisites
Before running the API server, ensure that you have the following prerequisites in place:

**Local Environment**
- An existing database should be running. Make sure to set the following environment variables:
```
DB_HOSTNAME
DB_NAME
DB_SCHEMA
DB_USER
DB_PWD
DB_PORT
SQL_DRIVER
```

**For SN Azure Environment**
- To run the application in the DPSN environment, you need to configure the following environment variables:
```
SN_KEY_VAULT_URI
AZURE_TENANT_ID
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_USERNAME
AZURE_PASSWORD
AZURE_DATABASE
AZURE_HOSTNAME
AZURE_SCHEMA
DB_PORT
SQL_DRIVER
```
### Command Line
```bash
python pip install -r ./requirements.txt 
cd src/
python server.py
```

### Run Docker container
```bash
docker build Dockerfile
```


## Tech Stack 
The API Server uses a FastAPI WebServer and connects to a database using an ODBC connection, using the sql connection library `sqlalchemy`. The Microsoft Authentication Library is used to generate an AAD Token that authenticates the API requests.  

