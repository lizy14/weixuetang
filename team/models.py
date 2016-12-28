from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from userpage.models import Student
from homework.models import Course


class TeamPost(models.Model):
    course = models.ForeignKey(Course)
    author = models.ForeignKey(Student)
    author_nick = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    type = models.IntegerField()
    detail = models.TextField()
    contact = models.CharField(max_length=128)
    published = models.DateTimeField()
    last_update = models.DateTimeField(null=True, default=None)


@receiver(pre_save, sender=TeamPost)
def log_time(sender, instance, raw, **kwargs):
    if raw:
        return
    if not instance.published:
        instance.published = timezone.now()
    else:
        instance.last_update = timezone.now()
