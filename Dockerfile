# syntax=docker/dockerfile:1
FROM python:3.8.3-slim

WORKDIR /python-docker

RUN apt-get update \
    && apt-get -y install libpq-dev gcc postgresql-contrib python3-dev

COPY setup.py setup.py
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080
EXPOSE 5000
EXPOSE 5432

CMD ["python", "api_main.py"]