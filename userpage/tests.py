from codex.basetest import APITest

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
        self.assertNotEqual(resp.json()['code'], 0) # already
        self.user.xt_id = None
        self.user.save()
        resp = self.simulate('post', '/api/u/bind/', {
            'student_id': 'lizy14',
            'password': 'Mo Qunzhu'
        })
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.json()['code'], 0) # wrong pass
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
