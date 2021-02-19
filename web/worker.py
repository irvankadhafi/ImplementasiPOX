import os
from celery import Celery
from app import app

#Celery configuration
app.config['CELERY_BROKEN_URL'] = 'redis://redis:6379/0'
app.config['result_backend'] = 'redis://redis:6379/0'

#initialize Celery
celery = Celery('tasks', broker=app.config['CELERY_BROKEN_URL'], backend=app.config['result_backend'])
celery.conf.update(app.config)