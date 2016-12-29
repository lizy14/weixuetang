from celery import shared_task
from .models import Student
import logging
from WeLearn.tasks import update_student
import asyncio

__logger__ = logging.getLogger(__name__)


@shared_task
def t_flush_student(id, mute=True):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(update_student(
            Student.objects.get(pk=id), mute))
    except Exception as e:
        __logger__.exception(str(e))

from wechat.tasks import send_template
from codex.taskutils import *
from django.utils import timezone
from datetime import timedelta, date


@shared_task
def notify():
    for usr in Student.objects.filter(xt_id__isnull=False):
        notify_student(usr, 'homework')


def notify_student(usr, *args):
    [globals()['notify_student_' + arg](usr) for arg in args]


from homework.models import HomeworkStatus
from wechat.tasks import send_template


def notify_student_homework(usr):
    res = HomeworkStatus.objects.filter(
        student=usr,
        submitted=False
    )
    if usr.pref.s_work:
        [send_template(usr.open_id, ins, '', safe_apply_async, eta=timezone.now().replace(
            hour=23, minute=59, second=59, microsecond=0) - timedelta(minutes=usr.pref.s_ddl_ahead_time)) for ins in res]
    else:
        visit_requests(cancel_check)
