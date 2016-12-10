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
        loop.run_until_complete(update_student(Student.objects.get(xt_id=xt_id), mute))
    except Exception as e:
        __logger__.exception(str(e))

from wechat.tasks import send_template
