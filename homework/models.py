from django.db import models
from userpage.models import Student
from django_model_changes import ChangesMixin

# import logging
# __logger__ = logging.getLogger(name=__name__)


class Course(models.Model):
    xt_id = models.CharField(max_length=32)
    name = models.TextField()


class Homework(models.Model):
    xt_id = models.CharField(max_length=32)
    course = models.ForeignKey(Course)
    title = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()
    detail = models.TextField()
    attachment = models.TextField(null=True, default=None)


class HomeworkStatus(models.Model, ChangesMixin):
    student = models.ForeignKey(Student, db_index=True)
    homework = models.ForeignKey(Homework)
    submitted = models.BooleanField(default=False)
    graded = models.BooleanField(default=False)
    grading = models.TextField(null=True, default=None)
    grading_comment = models.TextField(null=True, default=None)
    graded_by = models.CharField(max_length=32, null=True, default=None)
    ignored = models.BooleanField(default=False)


class CourseStatus(models.Model, ChangesMixin):
    student = models.ForeignKey(Student, db_index=True)
    course = models.ForeignKey(Course)
    ignored = models.BooleanField(default=False)
