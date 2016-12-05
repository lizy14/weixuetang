from django.db import models
from codex.baseerror import LogicError

class Student(models.Model):
	open_id = models.CharField(max_length=64, unique=True, db_index=True)
	xt_id = models.CharField(max_length=32, unique=True, null=True, db_index=True)
	token = models.CharField(max_length=64, null=True)
	@classmethod
	def get_by_openid(cls, openid):
		try:
			return cls.objects.get(open_id=openid)
		except cls.DoesNotExist:
			raise LogicError('User not found.')

class Subscription(models.Model):
	student = models.ForeignKey(Student, db_index=True)
	
