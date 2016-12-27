from django.shortcuts import render
from userpage.models import *
from .models import *
from codex.apiview import APIView
from codex.baseerror import *
from codex.utils import *
from wechat.wrapper import WeChatView
from datetime import datetime
import logging
__logger__ = logging.getLogger(name=__name__)


def parse_date(dt_str):
    return datetime.strptime(dt_str, '%Y-%m-%d')

def wrap_homework_status_status(hwSt):
    return 2 if hwSt.graded else 1 if hwSt.submitted else 0


class UnfinishedList(APIView):

    def get(self):
        def wrap(hw):
            return {
                'homework_id': hw.id,
                'start_time': wrap_time(hw.start_time),
                'end_time': wrap_time(hw.end_time),
                'title': hw.title,
                'course_name': hw.course.name,
                'detail': hw.detail,
                'attachment': hw.attachment
            }

        result = HomeworkStatus.objects.filter(
            student__id=self.student.id,
            submitted=False,
            homework__end_time__gte=datetime.today(),
            ignored=False
        )
        return [wrap(hwStatus.homework) for hwStatus in result]


class List(APIView):

    def get(self):
        def wrap(hwSt):
            hw = hwSt.homework
            return {
                'homework_id': hw.id,
                'start_time': wrap_time(hw.start_time),
                'end_time': wrap_time(hw.end_time),
                'title': hw.title,
                'course_name': hw.course.name,
                'status': wrap_homework_status_status(hwSt)
            }

        result = HomeworkStatus.objects.filter(
            student__id=self.student.id,
            ignored=False
        ).order_by('-homework__start_time')

        # hack
        # 为保持接口兼容，start 字段有二义性
        # 与 limit 同时出现时，表示数目，供前端列表无限滚动
        # 与 end 同时出现时，表示日期，供前端日历显示
        try:
            start = int(self.input['start'])
            limit = int(self.input['limit'])
            result = result[start: start + limit]
        except ValueError:
            pass
        except KeyError:
            pass

        try:
            start = parse_date(self.input['start'])
            end = parse_date(self.input['end'])
            result = result.filter(
                homework__end_time__gte=start,
                homework__end_time__lte=end
            )
        except ValueError:
            pass
        except KeyError:
            pass


        return [wrap(hwSt) for hwSt in result]


class Detail(APIView):

    def get(self):
        def wrap(hwSt):
            hw = hwSt.homework
            return {
                'homework_id': hw.id,
                'start_time': wrap_time(hw.start_time),
                'end_time': wrap_time(hw.end_time),
                'title': hw.title,
                'course_name': hw.course.name,
                'status': wrap_homework_status_status(hwSt),
                'detail': hw.detail,
                'attachment': hw.attachment,
                'grade': hwSt.grading,
                'graded_by': hwSt.graded_by,
                'comment': hwSt.grading_comment,
            }
        self.check_input('homework_id')
        result = HomeworkStatus.objects.get(
            student__id=self.student.id,
            homework__id=self.input['homework_id']
        )
        return wrap(result)


class Mark(APIView):

    def post(self):
        self.check_input('ignore', 'homework_id')
        flag = int(self.input['ignore']) != 0
        if self.input['homework_id'] == 'all':
            ls = HomeworkStatus.objects.filter(
                student__id=self.student.id
            )
            for item in ls:
                item.ignored = flag
                item.save()
        else:
            ins = HomeworkStatus.objects.get(
                student__id=self.student.id,
                homework__id=self.input['homework_id']
            )
            ins.ignored = flag
            ins.save()
