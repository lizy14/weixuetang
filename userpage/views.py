from django.shortcuts import render
from codex.baseview import APIView
from codex.baseerror import *
from .models import Student, Preference
from homework.models import CourseStatus
import urllib.request
from .tasks import t_flush_student
from ztylearn.Util import register
from .fortunes import get_fortune


class UserBind(APIView):

    def validate_user(self):
        try:
            register(self.input['student_id'], self.input['password'])
        except:
            raise ValidateError('CaμsAPI fail')

    def get(self):
        result = Student.get_by_openid(self.request.session['openid']).xt_id
        if result is None:
            raise LogicError('Unbind.')
        return result

    def post(self):
        self.check_input('student_id', 'password')
        user = Student.get_by_openid(self.request.session['openid'])
        self.validate_user()
        user.xt_id = self.input['student_id']
        user.save()
        t_flush_student.delay(user.xt_id)

class UserUnBind(APIView):

    def post(self):
        self.check_input('student_id')
        user = Student.get_by_openid(self.request.session['openid'])
        user.xt_id = None
        user.save()

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
        pass # TODO
