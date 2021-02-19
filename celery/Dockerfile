FROM python:3-alpine

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0

RUN mkdir -p /usr/src/queue
WORKDIR /usr/src/queue
COPY requirements.txt /usr/src/queue

RUN pip install -r requirements.txt
COPY . /usr/src/queue

# production
ENTRYPOINT celery -A tasks worker -l INFO