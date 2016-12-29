from codex.basetest import *
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

    def test_list_ignored(self):
        test_id = Notice.objects.all()[0].course.id
        self.simulate('post', '/api/u/courses/',
                      {'course_id': test_id, 'ignore': 1})
        all_names = [item['course_name'] for item in self.simulate(
            'get', '/api/notice/list/').json()['data']]
        self.assertNotIn(Course.objects.get(id=test_id).name, all_names,
                         'ignore course fails')
        self.simulate('post', '/api/u/courses/',
                      {'course_id': test_id, 'ignore': 0})
        all_names = [item['course_name'] for item in self.simulate(
            'get', '/api/notice/list/').json()['data']]
        self.assertIn(Course.objects.get(id=test_id).name, all_names,
                      'unignore course fails')

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
