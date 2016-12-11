
from codex.baseview import APIView
from codex.baseerror import *

from .models import *

from homework.views import wrap_date


class List(APIView):

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
        try:
            start = int(self.input['start'])
            limit = int(self.input['limit'])
            result = result[start : start + limit]
        except ValueError:
            pass
        except KeyError:
            pass

        return [wrap(ntSt) for ntSt in result]


class Detail(APIView):

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

    def get(self):
        self.check_input('notice_id')
        ntSt = NoticeStatus.objects.get(
            student__id=self.student.id,
            notice__id=self.input['notice_id']
        )
        ntSt.read = True
        ntSt.save()
        return 0
