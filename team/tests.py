# -*- coding: utf-8 -*-
#
from codex.basetest import APITest
from .models import *
from .views import *
import logging
__logger__ = logging.getLogger(name=__name__)

class TeamTests(APITest):
    def test_course(self):
        resp = self.simulate('get', '/api/team/course/', {
            'course_id': 1
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        self.assertEqual(len(resp.json()['data']), 2)
        self.assertNotIn('last_update', resp.json()['data'][0])
        self.assertTrue(resp.json()['data'][0]['i_am_the_author'])
    def test_edit(self):
        resp = self.simulate('post', '/api/team/edit/', {
            'post_id': 5,
            'title': '',
            'detail': '',
            'type': 1,
            'contact': '',
            'author_nickname': ''
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        tp = TeamPost.objects.get(pk=5)
        self.assertIsNotNone(tp.last_update)
        self.assertEqual(tp.author_nick, '')
        resp = self.simulate('post', '/api/team/edit/', {
            'course_id': 1,
            'title': '1',
            'detail': '1',
            'type': 1,
            'contact': '1',
            'author_nickname': '1'
        })
        self.assertEqual(len(TeamPost.objects.all()), 3)
        resp = self.simulate('post', '/api/team/edit/', {
            'course_id': 1,
            'title': '1',
            'detail': '1',
            'type': 1,
            'contact': '1',
            'author_nickname': '1'
        })
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.json()['code'], 0)
        self.assertEqual(len(TeamPost.objects.all()), 3)
    def test_delete(self):
        resp = self.simulate('post', '/api/team/delete', {
            'post_id': 5
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        self.assertEqual(len(TeamPost.objects.all()), 1)
        with self.assertRaises(TeamPost.DoesNotExist):
            tp = TeamPost.objects.get(pk=5)
