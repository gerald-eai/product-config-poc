FROM --platform=arm64 python:3.10-slim-bullseye

RUN apt update -y  &&  apt upgrade -y && apt-get update 
RUN apt-get update && apt-get install -y freetds-dev unixodbc-dev 
# Set environment variables for the ODBC Driver installation

# Install required dependencies for the ODBC Driver
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gnupg2 \
        apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# Download and install the Microsoft ODBC Driver 17 for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN sleep 5
RUN apt-get update 
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
# optional: for bcp and sqlcmd
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN source ~/.bashrc
# optional: for unixODBC development headers
# RUN sudo apt-get install -y unixodbc-dev
ENV PYODBC_VERSION=4.0.39

WORKDIR /app 

COPY ./requirements.txt .
COPY ./src/ . 

# install python packages; disable cache
RUN pip install --no-cache-dir --upgrade pip & pip install --no-cache-dir -r requirements.txt

EXPOSE 8000:8000
EXPOSE 2222

CMD ["uvicorn", "server:api", "--host", "0.0.0.0", "--port", "8000"]