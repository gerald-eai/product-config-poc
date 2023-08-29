# :todo: Update contents when ready 
FROM --platform=arm64 python:3.10-slim-bullseye

RUN apt update -y  &&  apt upgrade -y && apt-get update 
# set working directory inside the container

WORKDIR /app 

COPY ./requirements.txt .
COPY ./src . 

RUN pip install --no-cahce-dir --upgrade pip & pip install --no-cache-dir -r requirements.txt

EXPOSE 8501:8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]