# -*- coding: utf-8 -*-
#
from django.shortcuts import render
from codex.apiview import *
from codex.baseerror import *
from .models import *
# import logging
# __logger__ = logging.getLogger(name=__name__)

class List(APIView):

    def get(self):
        def wrap(item):
            return {
                'lecture_id': item.id,
                'time': item.time,
                'place': item.place,
                'lecturer': item.lecturer,
                'title': item.title,
            }
        result = Lecture.objects.all()
        try:
            start = int(self.input['start'])
            limit = int(self.input['limit'])
            result = result[start: start + limit]
        except ValueError:
            pass
        except KeyError:
            pass
        return [wrap(it) for it in result]


class Detail(APIView):

    def get(self):
        def wrap(item):
            return {
                'lecture_id': item.id,
                'time': item.time,
                'place': item.place,
                'lecturer': item.lecturer,
                'title': item.title,
                'detail': item.detail
            }
        self.check_input('lecture_id')
        try:
            item = Lecture.objects.get(pk=self.input['lecture_id'])
        except Lecture.DoesNotExist:
            raise LogicError('Not Found.')
        return wrap(item)
