from django.db import models
from homework.models import *


class Notice(models.Model):
    course = models.ForeignKey(Course)
    title = models.TextField()
    content = models.TextField()
    publisher = models.CharField(max_length=32)
    publishtime = models.DateField()
