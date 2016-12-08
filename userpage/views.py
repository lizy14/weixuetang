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
        self.check_input('openid')
        return Student.get_by_openid(self.input['openid']).xt_id

    def post(self):
        self.check_input('code', 'student_id', 'password')
        user = Student.get_by_openid(self.input['openid'])
        self.validate_user()
        user.xt_id = self.input['student_id']
        user.save()
        t_flush_student.delay(user.xt_id)

class Fortune(APIView):

    def get(self):
        return get_fortune()
