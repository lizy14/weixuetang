from django.shortcuts import render
from codex.baseview import APIView
from codex.baseerror import *
from .models import Student
import urllib.request
import uuid


from ztylearn.Util import register

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
        self.check_input('openid', 'student_id', 'password')
        user = Student.get_by_openid(self.input['openid'])
        self.validate_user()
        user.xt_id = self.input['student_id']
        user.token = uuid.uuid4()
        user.save()
