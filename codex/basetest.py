from django.test import TestCase, RequestFactory
import json

class BaseTest(TestCase):
    fixtures = ['init.json']

    def __init__(self, *args):
        super(BaseTest, self).__init__(*args)
        self.factory = RequestFactory()

    def make_request(self, method, url, data={}):
        return getattr(self.factory, method)(url, data)

    def simulate(self, method, url, data={}):
        return getattr(self.client, method)(url, data)

from userpage.models import Student

class APITest(BaseTest):

    def __init__(self, *args):
        super(APITest, self).__init__(*args)

    def setUp(self):
        self.user = Student.objects.all()[0]

    def make_request(self, method, url, data={}):
        data.update({
            'code': 'wechat_code',
            'state': 'view'
        })
        request = super(APITest, self).make_request(method, url, data)
        request.session = {
            'code': 'wechat_code',
            'openid': self.user.open_id
        }
        return request

    def simulate(self, method, url, data={}):
        data.update({
            'code': 'wechat_code',
            'state': 'view'
        })
        session = self.client.session
        session.update({
            'code': 'wechat_code',
            'openid': self.user.open_id
        })
        session.save()
        return super(APITest, self).simulate(method, url, data)
