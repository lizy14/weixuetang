from codex.basetest import APITest
from .models import *


class NoticeTests(APITest):

    def test_list(self):
        resp = self.simulate('get', '/api/notice/list/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        # unbind
        self.user.xt_id = None
        self.user.save()
        resp = self.simulate('get', '/api/notice/list/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 10)

    def test_detail(self):
        resp = self.simulate('get', '/api/notice/detail/', {'notice_id': 1})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)

    def test_make_as_read(self):
        self.assertFalse(NoticeStatus.objects.get(
            student=self.user, notice__id=1).read)
        resp = self.simulate(
            'get', '/api/notice/mark-as-read/', {'notice_id': 1})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        self.assertTrue(NoticeStatus.objects.get(
            student=self.user, notice__id=1).read)
