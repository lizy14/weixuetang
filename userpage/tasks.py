from celery import shared_task
from .models import Student
import logging
from WeLearn.tasks import update_student
import asyncio

__logger__ = logging.getLogger(__name__)


@shared_task
async def t_flush_student(xt_id):
    try:
        update_student(Student.objects.get(xt_id=xt_id))
    except Exception as e:
        __logger__.exception(str(e))
