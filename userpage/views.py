# -*- coding: utf-8 -*-
#
from django.shortcuts import render
from codex.apiview import *
from codex.baseerror import *
from .models import Student, Preference
from homework.models import CourseStatus
import urllib.request
from .tasks import t_flush_student
from ztylearn.Util import register
from .fortunes import get_fortune


class UserBind(BaseAPI):

    def validate_user(self):
        try:
            register(self.input['student_id'], self.input['password'])
        except:
            raise ValidateError('CaμsAPI fail')

    @BindMeta.bind_required
    def get(self):
        return self.student.xt_id

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


class Fortune(BaseAPI):

    def get(self):
        return get_fortune()


class UserPreference(APIView):

    def get(self):
        user = self.student
        pref = Preference.objects.get(student=user)
        return {
            's_work': pref.s_work,
            's_notice': pref.s_notice,
            's_grading': pref.s_grading,
            's_academic': pref.s_academic,
            's_lecture': pref.s_lecture,
            's_class_ahead_time': pref.s_class_ahead_time,
            's_ddl_ahead_time': pref.s_ddl_ahead_time
        }

    def post(self):
        # CHANGED: no longer requires all fields
        pref = Preference.objects.get(student=self.student)
        for arg in ('s_class_ahead_time', 's_ddl_ahead_time'):
            try:
                setattr(pref, arg, self.input[arg])
            except KeyError:
                pass

        for arg in ('s_work', 's_notice', 's_grading', 's_academic', 's_lecture'):
            try:
                setattr(pref, arg, int(self.input[arg]) != 0)  # '0'/'1' -> Bool
            except KeyError:
                pass
        pref.save()

from homework.models import Course, CourseStatus


class Courses(APIView):

    def get(self):
        def wrap(cst):
            return {
                'course_id': cst.course.id,
                'course_name': cst.course.name,
                'ignored': cst.ignored
            }
        ls = CourseStatus.objects.filter(student=self.student)
        return [wrap(item) for item in ls]

    def post(self):
        self.check_input('course_id', 'ignore')
        item = CourseStatus.objects.get(
            student=self.student,
            course__id=self.input['course_id']
        )
        item.ignored = int(self.input['ignore']) != 0
        item.save()
