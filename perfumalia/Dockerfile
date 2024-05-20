FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev pkg-config

WORKDIR /code

COPY requirements.txt /code

RUN pip install -r requirements.txt

COPY . /code

EXPOSE 8000