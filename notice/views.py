
from codex.baseview import APIView
from codex.baseerror import *

from .models import *

from homework.views import wrap_date, token_required


class List(APIView):
    @token_required
    def get(self):
        def wrap(ntSt):
            nt = ntSt.notice
            return {
                'notice_id'   : nt.id,
                'publisher'   : nt.publisher,
                'publish_time': wrap_date(nt.publishtime),
                'title'       : nt.title,
                'course_name' : nt.course.name,
                'detail'      : nt.content,
                'status'      : 1 if ntSt.read else 0
            }

        result = NoticeStatus.objects.filter(
            student__id=self.student.id
        )
        return [wrap(ntSt) for ntSt in result]


class Detail(APIView):
    @token_required
    def get(self):
        self.check_input('notice_id')

        def wrap(ntSt):
            nt = ntSt.notice
            return {
                'notice_id'   : nt.id,
                'publisher'   : nt.publisher,
                'publish_time': wrap_date(nt.publishtime),
                'title'       : nt.title,
                'course_name' : nt.course.name,
                'detail'      : nt.content,
                'status'      : ntSt.read
            }

        result = NoticeStatus.objects.get(
            student__id=self.student.id,
            notice__id=self.input['notice_id']
        )
        return wrap(result)


class MarkAsRead(APIView):
    @token_required
    def get(self):
        self.check_input('notice_id')
        ntSt = NoticeStatus.objects.get(
            student__id=self.student.id,
            notice__id=self.input['notice_id']
        )
        ntSt.read = True
        ntSt.save()
        return 0
