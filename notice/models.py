from django.db import models
from homework.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    read = models.BooleanField(default=False)


@receiver(post_save, sender=Notice)
def create_status(sender, instance, **kwargs):
    try:
        NoticeStatus.objects.get_or_create(
            notice=instance,
            student=instance._student,
        )
    except:
        pass
