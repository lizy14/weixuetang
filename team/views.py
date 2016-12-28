# -*- coding: utf-8 -*-
#
from django.shortcuts import render
from codex.apiview import *
from codex.baseerror import *
from .models import TeamPost
from homework.models import Course
from codex.utils import wrap_time as wrap_datetime
# import logging
# __logger__ = logging.getLogger(name=__name__)


class List(APIView):

    def get(self):
        def wrap(d):
            nonlocal self
            dat = {
                'post_id': d.id,
                'title': d.title,
                'type': d.type,
                'detail': d.detail,
                'contact': d.contact,
                'author_nickname': d.author_nick,
                'i_am_the_author': d.author == self.student,
                'published': wrap_datetime(d.published)
            }
            if d.last_update:
                dat['last_update'] = wrap_datetime(d.last_update)
            return dat
        self.check_input('course_id')
        ls = TeamPost.objects.filter(course__id=self.input['course_id'])
        return [wrap(d) for d in ls]


class Edit(APIView):

    def post(self):
        def identical(a, b, *fields):
            for k in fields:
                if str(getattr(a, k)) != str(getattr(b, k)):
                    return False
            return True
        create = False
        course = None
        try:
            self.check_input('course_id')
            course = Course.objects.get(pk=self.input['course_id'])
            create = True
        except InputError:
            self.check_input('post_id')
        self.check_input('title', 'type', 'detail',
                         'contact', 'author_nickname')
        if create:
            tp = TeamPost(author=self.student, course=course)
        else:
            tp = TeamPost.objects.get(pk=self.input['post_id'])
        tp.__dict__.update({
            'title': self.input['title'],
            'type': self.input['type'],
            'detail': self.input['detail'],
            'contact': self.input['contact'],
            'author_nick': self.input['author_nickname']
        })
        for it in TeamPost.objects.filter(author=self.student, course=course):
            if identical(it, tp, 'title', 'type', 'detail', 'contact', 'author_nick'):
                raise LogicError('Already exists.')
        tp.save()


class Delete(APIView):

    def post(self):
        self.check_input('post_id')
        tp = TeamPost.objects.get(pk=self.input['post_id'])
        assert tp.author == self.student
        tp.delete()
