from django.db import models
from userpage.models import *


class PersonalCalendar(models.Model):
    classes = models.TextField()  # JSON string, quick and dirty
    student = models.ForeignKey(Student)
