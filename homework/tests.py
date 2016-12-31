from codex.basetest import APITest
from .models import *
import logging

__logger__ = logging.getLogger(name=__name__)


class HomeworkTests(APITest):

    def test_detail(self):
        resp = self.simulate('get', '/api/hw/detail/')
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.json()['code'], 0)
        resp = self.simulate('get', '/api/hw/detail/', {'homework_id': 1})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)

    def test_unfinished_list(self):
        resp = self.simulate('get', '/api/hw/unfinished-list/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        [self.assertFalse(HomeworkStatus.objects.get(student=self.user, id=item['homework_id']).submitted)
         for item in resp.json()['data']]

    def test_list(self):
        resp = self.simulate('get', '/api/hw/list/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)

    def test_mark(self):
        resp = self.simulate('post', '/api/hw/mark/',
                             {'ignore': 1, 'homework_id': 1})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        self.assertTrue(HomeworkStatus.objects.get(
            student=self.user, homework__id=1).ignored)
        resp = self.simulate('post', '/api/hw/mark/',
                             {'ignore': 0, 'homework_id': 'all'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        [self.assertFalse(item.ignored)
         for item in HomeworkStatus.objects.filter(student=self.user)]

    def test_ignored(self):
        all_hst = HomeworkStatus.objects.all()
        matt = int(len(all_hst) / 2)
        for i in range(0, matt):
            all_hst[i].ignored = True
            all_hst[i].save()
        resp = self.simulate('get', '/api/hw/ignored-list/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        self.assertEqual(len(resp.json()['data']), matt)
        for it in resp.json()['data']:
            self.assertTrue(HomeworkStatus.objects.get(
                student=self.user, homework__id=it['homework_id']))
