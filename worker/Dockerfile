FROM python:3-alpine

RUN apk add --no-cache git gcc libc-dev make help2man
ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0

RUN mkdir -p /usr/src/celery
WORKDIR /usr/src/celery
COPY requirements.txt /usr/src/celery

RUN pip install -r requirements.txt
RUN pip install --upgrade python-iptables
COPY . /usr/src/celery
RUN make install
RUN export PYTHONPATH=$PYTHONPATH:/usr/src/celery/mininet
RUN export PATH=$PATH:/usr/src/celery/mininet
# production
ENTRYPOINT celery -A tasks worker -l INFO
