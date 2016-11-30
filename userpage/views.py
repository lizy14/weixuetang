from django.shortcuts import render
from codex.baseview import APIView
from codex.baseerror import *
from .models import Student
import urllib.request
import uuid

class UserBind(APIView):

    def validate_user(self):
        data = {
            'username': self.input['student_id'],
            'password': self.input['password']
        }
        res = eval(urllib.request.urlopen(urllib.request.Request(
			url='https://its.tsinghua.edu.cn/loginAjax',
			data=urllib.parse.urlencode(data).encode('utf-8'),
			method='POST')).read().decode())
        if res['code'] is not 0:
            raise ValidateError(res['msg'])

    def get(self):
        self.check_input('openid')
        return Student.get_by_openid(self.input['openid']).xt_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = Student.get_by_openid(self.input['openid'])
        self.validate_user()
        user.xt_id = self.input['student_id']
        user.xt_pw = self.input['password']
        user.xt_token = uuid.uuid4()
        user.save()
