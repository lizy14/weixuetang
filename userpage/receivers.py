from django.db.models.signals import pre_save, post_save
from .models import *
from django.dispatch import receiver
from homework.models import *

@receiver(pre_save, sender=Student)
def create_preference(sender, instance, raw, **kwargs):
    if raw:
        return
    if not instance.id:
        instance.pref = Preference.objects.create()

@receiver(post_save, sender=Preference)
def modified_pref(sender, instance, created, **kwargs):
    if created:
        return
    def hw_ddl_ahead_changed(tup):
        works = HomeworkStatus.objects.filter(student=instance.student, ignored=False)
        for work in works:
            work.ignored = True
            work.save()
        # NOTE: 假设django的dispatcher是按顺序分发处理的
        for work in works:
            work.ignored = False
            work.save()
    if 's_ddl_ahead_time' in instance.changes():
        hw_ddl_ahead_changed(instance.changes()['s_ddl_ahead_time'])
