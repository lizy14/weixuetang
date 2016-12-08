from django.shortcuts import render
from codex.baseview import APIView
from codex.baseerror import *
from .models import Student
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
        # t_flush_student.delay(user.xt_id)

class UserUnBind(APIView):

    def post(self):
        self.check_input('student_id')
        user = Student.get_by_openid(self.request.session['openid'])
        user.xt_id = None
        user.save()

class Fortune(APIView):

    def get(self):
        return get_fortune()
