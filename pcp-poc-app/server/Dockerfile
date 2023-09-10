FROM --platform=arm64 python:3.8-slim-bullseye

USER root

RUN apt-get update && apt-get install -y freetds-dev unixodbc-dev 
# Set environment variables for the ODBC Driver installation

# Install required dependencies for the ODBC Driver
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gcc gnupg2 \
        apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc

#Debian 11
RUN curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
# optional: for bcp and sqlcmd
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools18
RUN apt-get clean
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
# Add the mssql-tools18 binary to the PATH
ENV PATH="$PATH:/opt/mssql-tools18/bin"
RUN apt-get install -y libgssapi-krb5-2

# Install the CA certificates bundle
RUN apt-get update && apt-get install -y ca-certificates


WORKDIR /app 

COPY ./requirements.txt .
COPY ./src/ . 

# install python packages; disable cache
RUN pip install --no-cache-dir --upgrade pip & pip install --no-cache-dir -r requirements.txt

EXPOSE 8000:8000
EXPOSE 2222

CMD ["uvicorn", "server:api", "--host", "0.0.0.0", "--port", "8000"]