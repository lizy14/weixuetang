from django.db import models
from notice.models import Notice
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import Parser
# import logging
# __logger__ = logging.getLogger(name=__name__)

class Lecture(models.Model):
    time = models.CharField(max_length=128, null=True)
    place = models.CharField(max_length=128, null=True)
    lecturer = models.CharField(max_length=128, null=True)
    title = models.CharField(max_length=128)
    origin = models.ForeignKey(Notice)

    @property
    def detail(self):
        return self.origin.content

from wechat.tasks import send_template

@receiver(post_save, sender=Notice)
def create_lecture(sender, instance, **kwargs):
    if instance.course.name.startswith('文化素质教育讲座'):
        title, dic = Parser.parse(instance.title, instance.content)
        if not dic:
            return
        lec = Lecture.objects.get_or_create(time=dic.get('time', None), place=dic.get(
            'place', None), lecturer=dic.get('lecturer', None), title=title, origin=instance)
        try:
            if instance._student.pref.s_lecture and not instance._student.flushing:
                send_template(instance._student.open_id, lec)
        except:
            pass
