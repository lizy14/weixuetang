from codex.basetest import APITest
import logging
__logger__ = logging.getLogger(name=__name__)
from homework.models import CourseStatus
import json
from .models import *
from .views import *

class UserpageTests(APITest):

    def test_bind_get(self):
        resp = self.simulate('get', '/api/u/bind/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        self.user.xt_id = None
        self.user.save()
        resp = self.simulate('get', '/api/u/bind/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 10)

    def test_bind_post(self):
        resp = self.simulate('post', '/api/u/bind/', {
            'student_id': 'lizy14',
            'password': 'Mo Qunzhu'
        })
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.json()['code'], 0)  # already
        self.user.xt_id = None
        self.user.save()
        resp = self.simulate('post', '/api/u/bind/', {
            'student_id': 'lizy14',
            'password': 'Mo Qunzhu'
        })
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.json()['code'], 0)  # wrong pass
        from unittest.mock import patch
        with patch.object(UserBind, 'validate_user', return_value=True):
            resp = self.simulate('post', '/api/u/bind/', {
                'student_id': 'lizy14',
                'password': 'Mo Qunzhu'
            })
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json()['code'], 0)  # correct pass
            self.assertEqual(Student.objects.get(id=self.user.id).xt_id, 'lizy14')

    def test_unbind(self):
        resp = self.simulate('post', '/api/u/unbind/')
        from .models import Student
        self.user = Student.objects.all()[0]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        self.assertIsNone(self.user.xt_id)

    def test_fortune(self):
        resp = self.simulate('get', '/api/u/fortune/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)

    def test_courses_get(self):
        obj = CourseStatus.objects.get(student=self.user, course__id=1)
        obj.ignored = True
        obj.save()
        resp = self.simulate('get', '/api/u/courses/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        expected = json.loads('[{"course_id": 1, "course_name": "财务分析基础", "ignored": true}, {"course_id": 2, "course_name": "文化素质教育讲座（1）", "ignored": false}, {"course_id": 3, "course_name": "计算机与网络体系结构(1)", "ignored": false}, {"course_id": 4, "course_name": "计算机与网络体系结构（2）", "ignored": false}, {"course_id": 5, "course_name": "经济学", "ignored": false}, {"course_id": 6, "course_name": "软件工程（3）", "ignored": false}, {"course_id": 7, "course_name": "软件理论基础(2):函数式语言程序设计", "ignored": false}, {"course_id": 8, "course_name": "三年级男生羽毛球", "ignored": false}, {"course_id": 9, "course_name": "模式识别基础", "ignored": false}, {"course_id": 10, "course_name": "投资学", "ignored": false}, {"course_id": 11, "course_name": "西方文明史", "ignored": false}]')
        self.assertJSONEqual(json.dumps(resp.json()['data']), expected)

    def test_courses_post(self):
        resp = self.simulate('post', '/api/u/courses/',
                             {'course_id': 1, 'ignore': 1})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        self.assertTrue(CourseStatus.objects.get(
            student=self.user, course__id=1).ignored)
        resp = self.simulate('post', '/api/u/courses/',
                             {'course_id': 1, 'ignore': 0})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        self.assertFalse(CourseStatus.objects.get(
            student=self.user, course__id=1).ignored)

    def test_pref_get(self):
        resp = self.simulate('get', '/api/u/pref/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        self.assertJSONEqual(json.dumps(resp.json()['data']), json.loads(
            '{"s_lecture": true, "s_class_ahead_time": 20, "s_notice": true, "s_work": true, "s_ddl_ahead_time": 60, "s_grading": true}'))

    def test_pref_post(self):
        resp = self.simulate('post', '/api/u/pref/', {
            's_lecture': 0,
            's_notice': 1,
            's_class_ahead_time': 200,
            's_work': 1,
            's_ddl_ahead_time': 600,
            's_grading': 1
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        pref = self.user.pref
        self.assertTrue(pref.s_notice)
        self.assertTrue(pref.s_work)
        self.assertTrue(pref.s_grading)
        self.assertFalse(pref.s_lecture)
        self.assertEqual(pref.s_class_ahead_time, 200)
        self.assertEqual(pref.s_ddl_ahead_time, 600)
