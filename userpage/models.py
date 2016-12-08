from django.db import models
from codex.baseerror import LogicError

class Student(models.Model):
	open_id = models.CharField(max_length=64, unique=True, db_index=True)
	xt_id = models.CharField(max_length=32, unique=True, null=True, db_index=True)
	@classmethod
	def get_by_openid(cls, openid):
		try:
			return cls.objects.get(open_id=openid)
		except cls.DoesNotExist:
			raise LogicError('User not found.')

class Preference(models.Model):
	student = models.ForeignKey(Student, db_index=True)
	s_work = models.BooleanField(default=True)
	s_notice = models.BooleanField(default=True)
	s_academic = models.BooleanField(default=True)
	s_lecture = models.BooleanField(default=True)
	s_class = models.BooleanField(default=True)
	s_grading = models.BooleanField(default=True)
	ahead_time = models.IntegerField()
