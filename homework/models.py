from django.db import models
from userpage.models import *

class Course(models.Model):
    xt_id = models.CharField(max_length=32)
    name = models.CharField(max_length=32)


class Homework(models.Model):
    xt_id = models.CharField(max_length=32, db_index=True)
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=32)
    start_time = models.DateField()
    end_time = models.DateField()
    detail = models.CharField(max_length=1024)


class HomeworkStatus(models.Model):
    student = models.ForeignKey(Student, db_index=True)
    homework = models.ForeignKey(Homework)
    submitted = models.BooleanField()
    graded = models.BooleanField()
    grading = models.CharField(max_length=1024)


class CourseStatus(models.Model):
    student = models.ForeignKey(Student, db_index=True)
    course = models.ForeignKey(Course)
