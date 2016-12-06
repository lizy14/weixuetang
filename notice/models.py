from django.db import models
from homework.models import *


class Notice(models.Model):
    course = models.ForeignKey(Course)
    xt_id = models.CharField(max_length=32, default=None)

    title = models.TextField()
    content = models.TextField()
    publisher = models.CharField(max_length=32)
    publishtime = models.DateField()


class NoticeStatus(models.Model):
    notice = models.ForeignKey(Notice)
    student = models.ForeignKey(Student)

    read = models.BooleanField()
