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


from django.db.models.signals import post_save
from django.dispatch import receiver
from wechat.tasks import *
from codex.taskutils import *
from django.utils import timezone
from datetime import datetime, time, timedelta
import logging
logger = logging.getLogger(name=__name__)


@receiver(post_save, sender=HomeworkStatus)
def update_hw_status(sender, instance, created, **kwargs):
    def graded(tup):
        nonlocal instance
        if not instance.student.pref.s_grading:
            return
        send_template(instance.student.open_id, instance)

    def ignored(tup):
        nonlocal instance
        ahead = instance.student.pref.s_ddl_ahead_time
        eta = timezone.make_aware(datetime.combine(instance.homework.end_time, time(
            23, 59, 59)) - timedelta(minutes=ahead))
        if eta < timezone.now() or ahead < 0:
            return
        if tup[1]:
            revoke_send(instance.student.open_id,
                        instance.homework, '', eta=eta)
        elif instance.student.pref.s_work:
            send_template(instance.student.open_id,
                          instance.homework, '', safe_apply_async, eta=eta)
    def ddl_changed(tup):
        nonlocal instance
        ahead=instance.student.pref.s_ddl_ahead_time
        eta=timezone.make_aware(datetime.combine(tup[0], time(
            23, 59, 59)) - timedelta(minutes=ahead))
        revoke_send(instance.student.open_id,
                    instance.homework, '', eta=eta)
        eta=timezone.make_aware(datetime.combine(instance.homework.end_time, time(
            23, 59, 59)) - timedelta(minutes=ahead))
        if eta < timezone.now() or ahead < 0:
            return
        send_template(instance.student.open_id,
                      instance.homework, '', safe_apply_async, eta=eta)
    if created:
        ignored((0, 0))
        return
    for k, v in instance.changes().items():
        if k == 'graded':
            graded(v)
        elif k == 'ignored':
            ignored(v)
        elif k == 'end_time':
            ddl_changed(v)



from userpage.models import Student


@receiver(post_save, sender=Homework)
def create_hw_status(sender, instance, created, **kwargs):
    try:
        status=HomeworkStatus.objects.get(
            student=instance._status.student, homework__xt_id=instance.xt_id)
    except:
        status=HomeworkStatus(
            student=instance._status.student, homework=instance)
    status.__dict__.update({
        'submitted': instance._status.submitted,
        'graded': instance._status.graded,
        'grading': instance._status.grading,
        'grading_comment': instance._status.grading_comment,
        'graded_by': instance._status.graded_by,
    })
    status.save()

@receiver(post_save, sender=CourseStatus)
def modified_cs_status(sender, instance, created, **kwargs):
    def ignored(tup):
        nonlocal instance
        works=HomeworkStatus.objects.filter(
            student=instance.student, homework__course=instance.course)
        for work in works:
            work.ignored=tup[1]
            work.save()
    if created:
        return
    if 'ignored' in instance.changes():
        ignored(instance.changes()['ignored'])
