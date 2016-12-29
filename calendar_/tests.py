from codex.basetest import APITest
from .models import *
import logging
__logger__ = logging.getLogger(name=__name__)

class CalendarTest(APITest):
    def test_global(self):
        resp = self.simulate('get', '/api/cal/global/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
    def test_personal(self):
        resp = self.simulate('get', '/api/cal/personal/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
    def test_semester(self):
        resp = self.simulate('get', '/api/cal/semester/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
