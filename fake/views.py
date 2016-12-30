from codex.apiview import BaseAPI


class FakeAPI(BaseAPI):

    def do_dispatch(self, *args, **kwargs):
        self.input = self.query or self.body
        handler = getattr(self, self.request.method.lower(), None)
        if not callable(handler):
            return self.http_method_not_allowed()
        return self.api_wrapper._original(self, handler, *args, **kwargs)

from homework.models import Course, Homework
from datetime import date

class NewHomework(FakeAPI):

    def post(self):
        self.check_input('title')
        软工 = Course.objects.get(name='软件工程（3）')
        hw = Homework(title=self.input['title'], start_time=date.today(), end_time=date.today(), detail='这是一条测试用作业，没有布置到网络学堂上，请放心。\n膜群主小组祝您生活愉快！', course=软工)
        hw.force_now = True
        hw.save()
