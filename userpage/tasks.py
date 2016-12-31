from celery import shared_task
from .models import Student
import logging
from WeLearn.tasks import update_student
import asyncio

__logger__ = logging.getLogger(__name__)


@shared_task
def t_flush_student(id):
    try:
        stu = Student.objects.get(pk=id)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(update_student(stu))
        stu.flushing = False
        stu.save()
    except Exception as e:
        __logger__.exception(str(e))
