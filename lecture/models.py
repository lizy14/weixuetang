from django.db import models
from notice.models import Notice
from django.db.models.signals import post_save
from django.dispatch import receiver

class Lecture(models.Model):
    time = models.CharField(max_length=128)
    place = models.CharField(max_length=128)
    lecturer = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    origin = models.ForeignKey(Notice)
    @property
    def detail(self):
        return self.origin.content

@receiver(post_save, sender=Notice)
def create_preference(sender, instance, **kwargs):
    pass
