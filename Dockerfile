FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN apt-get update \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8000
CMD alembic upgrade head \
    && uvicorn --host=0.0.0.0 --reload app.main:app
