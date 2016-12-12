# -*- coding: utf-8 -*-
#
from django.db import models


class Template(models.Model):
    t_id = models.CharField(max_length=50, unique=True)
    t_title = models.TextField()

    @classmethod
    def get_template_id(cls, name):
        try:
            return cls.objects.get(t_title=name).t_id
        except cls.DoesNotExist:
            raise LogicError('Template not found.')
