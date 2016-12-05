# -*- coding: utf-8 -*-
#
from __future__ import absolute_import
import os
from celery import Celery
from . import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeLearn.settings')
app = Celery('WeLearn')
app.config_from_object('WeLearn:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# import django
# django.setup()
