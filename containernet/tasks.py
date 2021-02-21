import os
import time
from celery import Celery
# import topology yang dibuat mas mas its
import lordy

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task(name='tasks.add')
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y
@celery.task(name='tasks.myNetworks')
def myNetworks():
    lordy.myNetwork()

@celery.task
def tambahdockers(idDocker,ipDocker,imageDocker,switch):
    lordy.tambahDocker(idDocker,ipDocker,imageDocker,switch)

@celery.task
def tesNets():
    lordy.lordyNet()

@celery.task
def addSwitchs(source_id):
    lordy.lordyAddSwitch(source_id)

@celery.task
def tambahlinks(source,dest):
    lordy.lordyAddLink(source,dest)

@celery.task
def delLinks(source,dest):
    lordy.lordyDelLink(source,dest)