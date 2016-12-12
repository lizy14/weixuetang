from celery import shared_task
from .models import Student
import logging
from WeLearn.tasks import update_student
import asyncio

__logger__ = logging.getLogger(__name__)


@shared_task
def t_flush_student(xt_id, mute=True):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(update_student(
            Student.objects.get(xt_id=xt_id), mute))
    except Exception as e:
        __logger__.exception(str(e))

from wechat.tasks import send_template
from celery import current_app
from celery.app.control import Inspect
from dateutil import parser
from django.utils import timezone
from datetime import timedelta


def safe_apply_async(task, args=None, kwargs={}, **options):
    schedule = Inspect(app=current_app).scheduled()
    for k, v in schedule.items():
        for item in v:
            req = item['request']
            if req['name'] == task.name and req['args'] == str(list(args)) and req['kwargs'] == str(kwargs) and (not (getattr(options, 'eta', False) and options['eta'] != parser.parse(req['eta']))):
                return
    task.apply_async(args, kwargs, **options)


@shared_task
def notify():
    for usr in Student.objects.all():
        notify_student(usr)


@shared_task
def notify_student():
    pass
