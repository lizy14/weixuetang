from django.db import models
from userpage.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_model_changes import ChangesMixin

import logging
__logger__ = logging.getLogger(name=__name__)


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

from wechat.tasks import send_template, t_send_template
# from userpage.models import Student
from codex.taskutils import *
from django.utils import timezone
from datetime import datetime, time, timedelta


@receiver(post_save, sender=HomeworkStatus)
def update_hw_status(sender, instance, raw, **kwargs):
    if raw:
        return

    def graded(tup):
        nonlocal instance
        send_template(instance.student.openid, instance)

    def ignored(tup):
        nonlocal instance
        if tup[1]:
            # revoke(t_send_template, args=None)
            pass
        else:
            ahead = instance.student.pref.s_ddl_ahead_time
            eta = datetime.combine(instance.homework.end_time, time(
                23, 59, 59)) - timedelta(minutes=ahead) if not getattr(instance, 'force_now', False) else datetime.now() + timedelta(seconds=10)
            __logger__.critical(eta)
            send_template(instance.student.open_id, instance.homework, '', safe_apply_async, eta=eta)

    for k, v in instance.changes().items():
        if k == 'graded':
            graded(v)
        elif k == 'ignored':
            ignored(v)
        else:
            pass
    # if 'ignored' not in instance.changes():
        # ignored((0, 0))
    if instance.force_now:
        ignored((0, 0))

class CourseStatus(models.Model):
    student = models.ForeignKey(Student, db_index=True)
    course = models.ForeignKey(Course)
    ignored = models.BooleanField(default=False)

from userpage.models import Student

@receiver(post_save, sender=Homework)
def create_hw_status(sender, instance, raw, **kwargs):
    if raw:
        return
    subscribes = CourseStatus.objects.filter(course=instance.course)
    for sub in subscribes:
        stu = sub.student
        try:
            _ = HomeworkStatus.objects.get(student=stu, homework=instance)
        except:
            hws = HomeworkStatus(student=stu, homework=instance)
            if getattr(instance, 'force_now', False):
                hws.force_now = True
            hws.save()
