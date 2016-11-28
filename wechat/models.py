# -*- coding: utf-8 -*-
#
from django.db import models
from codex.baseerror import LogicError


class Student(models.Model):
	open_id = models.CharField(max_length=64, unique=True, db_index=True)
	student_id = models.CharField(max_length=32, unique=True, null=True, db_index=True)
	@classmethod
	def get_by_openid(cls, openid):
		try:
			return cls.objects.get(open_id=openid)
		except cls.DoesNotExist:
			raise LogicError('User not found.')
