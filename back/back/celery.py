from __future__ import absolute_import
from django.conf import settings
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')


app = Celery('back')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(settings.INSTALLED_APPS)

if __name__ == '__main__':
    app.start()
