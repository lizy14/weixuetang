from django.shortcuts import render
from userpage.models import *
from .models import *
from codex.baseview import APIView
from codex.baseerror import *
from wechat.wrapper import WeChatView
from datetime import datetime


def wrap_date(d):
    return d.strftime('%Y-%m-%d')


def wrap_homework_status_status(hwSt):
    return 2 if hwSt.graded else 1 if hwSt.submitted else 0


class UnfinishedList(APIView):

    def get(self):
        def wrap(hw):
            return {
                'homework_id': hw.id,
                'start_time': wrap_date(hw.start_time),
                'end_time': wrap_date(hw.end_time),
                'title': hw.title,
                'course_name': hw.course.name,
                'detail': hw.detail,
                'attachment': hw.attachment
            }

        result = HomeworkStatus.objects.filter(
            student__id=self.student.id,
            submitted=False,
            homework__end_time__gte=datetime.today()
        )
        return [wrap(hwStatus.homework) for hwStatus in result]


class List(APIView):

    def get(self):
        def wrap(hwSt):
            hw = hwSt.homework
            return {
                'homework_id': hw.id,
                'start_time': wrap_date(hw.start_time),
                'end_time': wrap_date(hw.end_time),
                'title': hw.title,
                'course_name': hw.course.name,
                'status': wrap_homework_status_status(hwSt)
            }

        result = HomeworkStatus.objects.filter(
            student__id=self.student.id
        ).order_by('-homework__start_time')

        try:
            start = int(self.input['start'])
            limit = int(self.input['limit'])
            result = result[start : start + limit]
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
                'start_time': wrap_date(hw.start_time),
                'end_time': wrap_date(hw.end_time),
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
