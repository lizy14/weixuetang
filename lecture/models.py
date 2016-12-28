from django.db import models
from notice.models import Notice
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import Parser


class Lecture(models.Model):
    time = models.CharField(max_length=128, null=True)
    place = models.CharField(max_length=128, null=True)
    lecturer = models.CharField(max_length=128, null=True)
    title = models.CharField(max_length=128)
    origin = models.ForeignKey(Notice)

    @property
    def detail(self):
        return self.origin.content


@receiver(post_save, sender=Notice)
def create_lecture(sender, instance, **kwargs):
    if instance.course.name.startswith('文化素质教育讲座'):
        title, dic = Parser.parse(instance.title, instance.content)
        Lecture.objects.create(time=getattr(dic, 'time', None), place=getattr(
            dic, 'place', None), lecturer=getattr(dic, 'lecturer', None), title=title, origin=instance)
