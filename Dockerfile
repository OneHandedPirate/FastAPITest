FROM python:slim-buster
LABEL authors="onehandedpirate"

ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir /code
WORKDIR /code
COPY . /code/

EXPOSE 8000

CMD uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
