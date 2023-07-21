FROM --platform=arm64 python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y freetds-dev unixodbc-dev 

ENV PYODBC_VERSION=4.0.39

WORKDIR /app 

COPY ./requirements.txt .
COPY ./src/ . 

# install python packages; disable cache
RUN pip install --no-cache-dir --upgrade pip & pip install --no-cache-dir -r requirements.txt

EXPOSE 8000:8000
EXPOSE 2222

CMD ["uvicorn", "server:api", "--host", "0.0.0.0", "--port", "8000"]