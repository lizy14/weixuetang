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
from datetime import timedelta, date


def visit_requests(func):
    schedule = Inspect(app=current_app).scheduled()
    return [[func(item['request']) for item in v] for k, v in schedule.items()]


def safe_apply_async(task, args=None, kwargs={}, **options):
    def check(req):
        __logger__.info(req)
        nonlocal task, args, kwargs, options
        if req['name'] == task.name and eval(req['args']) == list(args) and eval(req['kwargs']) == kwargs and (not (getattr(options, 'eta', False) and options['eta'] != parser.parse(req['eta']))):
            raise
        return False # safe
    try:
        visit_requests(check)
        task.apply_async(args, kwargs, **options)
    except:
        return


@shared_task
def notify():
    for usr in Student.objects.all():
        notify_student(usr, 'homework')

@shared_task
def test():
    pass

def notify_student(usr, *args):
    # [globals()['notify_student_' + arg](usr) for arg in args]
    time = timezone.now() + timedelta(seconds=10)
    test.apply_async(eta=time)
    safe_apply_async(test, eta=time)


from homework.models import HomeworkStatus
from wechat.tasks import send_template

def notify_student_homework(usr):
    def cancel_check(req):
        nonlocal usr
        if eval(req['args'])[0] == usr.open_id:
            current_app.control.revoke(req['id'])

    res = HomeworkStatus.objects.filter(
        student=usr,
        submitted=False
    )
    if usr.pref.s_work:
        [send_template(usr.open_id, ins, '', safe_apply_async, eta=timezone.now().replace(hour=23, minute=59, second=59, microsecond=0)-timedelta(minutes=usr.pref.ahead_time)) for ins in res]
    else:
        visit_requests(cancel_check)
