from django.db import models
from codex.baseerror import LogicError
from django_model_changes import ChangesMixin


class Preference(models.Model, ChangesMixin):
    s_work = models.BooleanField(default=True)
    s_notice = models.BooleanField(default=True)
    s_lecture = models.BooleanField(default=True)
    s_grading = models.BooleanField(default=True)
    s_class_ahead_time = models.IntegerField(default=20)
    s_ddl_ahead_time = models.IntegerField(default=60)


class Student(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    xt_id = models.CharField(max_length=32, null=True, db_index=True)
    pref = models.OneToOneField(Preference, related_name='student')
    flushing = models.NullBooleanField()
    @classmethod
    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found.')
