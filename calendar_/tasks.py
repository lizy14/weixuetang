from celery import shared_task
from .models import get_appointments
from userpage.models import Student
from datetime import date, time, datetime, timedelta
from django.utils import timezone


class ClassInfo(object):

    def __init__(self, obj):
        self.title = obj['title']
        self.begin = timezone.make_aware(datetime.fromtimestamp(obj['begin']))
        self.end = timezone.make_aware(datetime.fromtimestamp(obj['end']))
        self.location = obj['location']

from wechat.tasks import send_template


@shared_task(name='calendar_.tasks.alert_class')
def alert_class():
    students = Student.objects.filter(xt_id__isnull=False)
    for stud in students:
        classes = get_appointments(stud.xt_id, datetime.combine(date.today(
        ), time.min), datetime.combine(date.today() + timedelta(days=1), time.min))
        for cls in classes:
            ins = ClassInfo(cls)
            send_template(stud.open_id, ins, eta=ins.begin)
