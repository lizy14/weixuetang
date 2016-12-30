from django.db import models
from codex.baseerror import LogicError
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Preference(models.Model):
    s_work = models.BooleanField(default=True)
    s_notice = models.BooleanField(default=True)
    s_academic = models.BooleanField(default=True)
    s_lecture = models.BooleanField(default=True)
    s_grading = models.BooleanField(default=True)
    s_class_ahead_time = models.IntegerField(default=20)
    s_ddl_ahead_time = models.IntegerField(default=60)


class Student(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    xt_id = models.CharField(max_length=32, null=True, db_index=True)
    pref = models.OneToOneField(Preference, related_name='student')
    @classmethod
    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found.')


@receiver(pre_save, sender=Student)
def create_preference(sender, instance, raw, **kwargs):
    if raw:
        return
    if not instance.id:
        instance.pref = Preference.objects.create()
