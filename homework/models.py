from django.db import models
from userpage.models import *

class Course(models.Model):
    xt_id = models.CharField(max_length=32)
    name = models.TextField()


class Homework(models.Model):
    xt_id = models.CharField(max_length=32, db_index=True)
    course = models.ForeignKey(Course)
    title = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()
    detail = models.TextField()


class HomeworkStatus(models.Model):
    student = models.ForeignKey(Student, db_index=True)
    homework = models.ForeignKey(Homework)
    submitted = models.BooleanField()
    graded = models.BooleanField()
    grading = models.TextField()


class CourseStatus(models.Model):
    student = models.ForeignKey(Student, db_index=True)
    course = models.ForeignKey(Course)
