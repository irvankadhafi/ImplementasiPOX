FROM python:3-alpine

# ENV CELERY_BROKER_URL redis://redis:6379/0
# ENV CELERY_RESULT_BACKEND redis://redis:6379/0

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN export PYTHONPATH=$PYTHONPATH:/usr/src/app/mininet
RUN export PATH=$PATH:/usr/src/app/mininet

# Expose the Flask port
EXPOSE 5000
RUN pip install gunicorn

# CMD [ "python", "./main.py" ]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "main:app"]