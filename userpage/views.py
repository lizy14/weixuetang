# -*- coding: utf-8 -*-
#
from django.shortcuts import render
from codex.apiview import APIView
from codex.baseerror import *
from .models import Student, Preference
from homework.models import CourseStatus
import urllib.request
from .tasks import t_flush_student
from ztylearn.Util import register
from .fortunes import get_fortune
from .utils import *


class UserBind(APIView):

    def validate_user(self):
        try:
            register(self.input['student_id'], self.input['password'])
        except:
            raise ValidateError('CaμsAPI fail')

    def get(self):
        result = self.student.xt_id
        if result is None:
            raise UnbindError()
        return result

    def post(self):
        if self.student.xt_id is not None:
            raise LogicError('Already bound.')
        self.check_input('student_id', 'password')
        self.validate_user()
        self.student.xt_id = self.input['student_id']
        self.student.save()
        t_flush_student.delay(self.student.xt_id)


class UserUnBind(APIView):

    def post(self):
        self.student.xt_id = None
        self.student.save()


class Fortune(APIView):

    def get(self):
        return get_fortune()


class UserPreference(APIView):

    def get(self):
        user = Student.get_by_openid(self.request.session['openid'])
        pref = Preference.objects.get(student=user)
        ignored = CourseStatus.objects.get(student=user, ignored=True)
        ls = [i.xt_id for i in ignored]
        return {
            's_work': pref.s_work,
            's_notice': pref.s_notice,
            's_grading': pref.s_grading,
            's_academic': pref.s_academic,
            's_lecture': pref.s_lecture,
            's_class': pref.s_class,
            'ignore_courses': ls,
            'ahead_time': pref.ahead_time
        }

    def post(self):
        # NOTE: plz post all data whether modified or not
        self.check_input('s_work', 's_notice', 's_grading', 's_academic',
                         's_lecture', 's_class', 'ignore_courses', 'ahead_time')
        pref = Preference.objects.get(student=self.student)
        update_fields(pref, self.input, 's_work', 's_notice', 's_grading',
                      's_academic', 's_lecture', 's_class', 'ahead_time')
        pref.save()
        allcls = CourseStatus.objects.filter(student=self.student)
        for cls in allcls:
            cls.ignored = True if cls.course.xt_id in self.input[
                'ignore_courses'] else False
            cls.save()
