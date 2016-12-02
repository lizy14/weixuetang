from django.shortcuts import render
from userpage.models import *
from .models import *
from codex.baseview import APIView
from codex.baseerror import *

from datetime import datetime


def wrap_date(d):
    return d.strftime('%Y-%m-%d')
    return datetime.combine(d, datetime.min.time()).timestamp()


def wrap_homework_status_status(hwSt):
    return 2 if hwSt.graded else 1 if hwSt.submitted else 0


def token_required(function=None):
    def wrapper(obj, *args, **kwargs):

        obj.check_input('student_id', 'token')
        xt_id = obj.input['student_id']
        token = obj.input['token']
        student = Student.objects.get(xt_id=xt_id)
        if token != student.token:
            raise InputError('Invalid token')
        obj.student = student

        return function(obj, *args, **kwargs)
    return wrapper


class UnfinishedList(APIView):
    @token_required
    def get(self):
        def wrap(hw):
            return {
                'id'         : hw.id,
                'start_time' : wrap_date(hw.start_time),
                'end_time'   : wrap_date(hw.end_time),
                'title'      : hw.title,
                'course_name': hw.course.name,
                'detail'     : hw.detail,
                'attachment' : ""  # TODO
            }

        result = HomeworkStatus.objects.filter(
            student__id=self.student.id,
            submitted=False,
            homework__end_time__gte=datetime.today()
        )
        return [wrap(hwStatus.homework) for hwStatus in result]


class List(APIView):
    @token_required
    def get(self):
        def wrap(hwSt):
            hw = hwSt.homework
            return {
                'id'         : hw.id,
                'start_time' : wrap_date(hw.start_time),
                'end_time'   : wrap_date(hw.end_time),
                'title'      : hw.title,
                'course_name': hw.course.name,
                'status'     : wrap_homework_status_status(hwSt)
            }

        result = HomeworkStatus.objects.filter(
            student__id=self.student.id
        )
        return [wrap(hwSt) for hwSt in result]


class Detail(APIView):
    @token_required
    def get(self):
        def wrap(hwSt):
            hw = hwSt.homework
            return {
                'id'         : hw.id,
                'start_time' : wrap_date(hw.start_time),
                'end_time'   : wrap_date(hw.end_time),
                'title'      : hw.title,
                'course_name': hw.course.name,
                'status'     : wrap_homework_status_status(hwSt),
                'detail'     : hw.detail,
                'attachment' : ""  # TODO
            }
        self.check_input('id')
        result = HomeworkStatus.objects.get(
            student__id=self.student.id,
            homework__id=self.input['id']
        )
        return wrap(result)
