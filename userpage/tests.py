from codex.basetest import APITest
import logging
__logger__ = logging.getLogger(name=__name__)


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

    def test_courses(self):
        from homework.models import CourseStatus
        obj = CourseStatus.objects.get(student=self.user, course__id=1)
        obj.ignored = True
        obj.save()
        resp = self.simulate('get', '/api/u/courses/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
        import json
        expected = json.loads('[{"course_id": 1, "course_name": "财务分析基础", "ignored": 1}, {"course_id": 2, "course_name": "文化素质教育讲座（1）", "ignored": 0}, {"course_id": 3, "course_name": "计算机与网络体系结构(1)", "ignored": 0}, {"course_id": 4, "course_name": "计算机与网络体系结构（2）", "ignored": 0}, {"course_id": 5, "course_name": "经济学", "ignored": 0}, {"course_id": 6, "course_name": "软件工程（3）", "ignored": 0}, {"course_id": 7, "course_name": "软件理论基础(2):函数式语言程序设计", "ignored": 0}, {"course_id": 8, "course_name": "三年级男生羽毛球", "ignored": 0}, {"course_id": 9, "course_name": "模式识别基础", "ignored": 0}, {"course_id": 10, "course_name": "投资学", "ignored": 0}, {"course_id": 11, "course_name": "西方文明史", "ignored": 0}]')
        self.assertJSONEqual(json.dumps(resp.json()['data']), expected)
