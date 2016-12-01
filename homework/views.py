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


class UnifinishedList(APIView):
    @token_required
    def get(self):
        def wrap_homework(hw):
            return {
                'id'         : hw.id,
                'start_time' : wrap_date(hw.start_time),
                'end_time'   : wrap_date(hw.end_time),
                'title'      : hw.title,
                'course_name': hw.course.name,
                'detail'     : hw.detail,
                'attachment' : "" # TODO
            }

        result = []
        for hwStatus in HomeworkStatus.objects.filter(student__id=self.student.id):
            if not hwStatus.submitted:
                result.append(wrap_homework(hwStatus.homework))
        return result


class List(APIView):
    @token_required
    def get(self):
        def wrap_homework_status(hwSt):
            hw = hwSt.homework
            return {
                'id'         : hw.id,
                'start_time' : wrap_date(hw.start_time),
                'end_time'   : wrap_date(hw.end_time),
                'title'      : hw.title,
                'course_name': hw.course.name,
                'status'     : wrap_homework_status_status(hwSt)
            }

        result = HomeworkStatus.objects.filter(student__id=self.student.id)
        return wrap_homework_status(result)



class Detail(APIView):
    @token_required
    def get(self):
        def wrap_homework_status(hwSt):
            hw = hwSt.homework
            return {
                'id'         : hw.id,
                'start_time' : wrap_date(hw.start_time),
                'end_time'   : wrap_date(hw.end_time),
                'title'      : hw.title,
                'course_name': hw.course.name,
                'status'     : wrap_homework_status_status(hwSt),
                'detail'     : hw.detail,
                'attachment' : "" # TODO
            }

        result = []
        for hwStatus in HomeworkStatus.objects.filter(student__id=self.student.id):
            result.append(wrap_homework_status(hwStatus))
        return result
