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
        debug = [{
            "detail": "",
            "start_time": "2016-11-27",
            "course_name": "\u6a21\u5f0f\u8bc6\u522b\u57fa\u7840",
            "title": "homework\u00a04",
            "end_time": "2016-12-12"
        }, {
            "detail": "\u5b9e\u9a8c\u4efb\u52a1\u5206\u4e3a\u4e09\u90e8\u5206\uff0c\u5176\u4e2d\u7b2c\u4e8c\u90e8\u5206\u4e3a\u5fc5\u505a\u3002\r\n\u7b2c\u4e00\u90e8\u5206\uff08\u4e0d\u8ba1\u5206\u6570\uff0c\u4e0d\u9700\u63d0\u4ea4\uff09\uff1a\u6309\u8981\u6c42\u7f16\u5199Y86\u6c47\u7f16\u7a0b\u5e8f\uff0c\u4f7f\u5176\u53ef\u4ee5\u5728\u6a21\u62df\u5668\u5185\u8fd0\u884c\u3002\r\n\u7b2c\u4e8c\u90e8\u5206\uff1a\u53ea\u4fee\u6539\u6a21\u62df\u5668\u5185\u7684hcl\u6587\u4ef6\uff0c\u5b9e\u73b0\u6307\u4ee4iaddl\u548cleave\u3002\r\n\u7b2c\u4e09\u90e8\u5206\uff08\u52a0\u5206\u9879\uff09\uff1a\u4fee\u6539\u6a21\u62df\u5668\u7a0b\u5e8f\uff0c\u5b9e\u73b0\u66f4\u591a\u6307\u4ee4\uff08\u4f8b\u5982rmxchg\uff09\u3002\u8981\u6c42\u53ef\u7f16\u8bd1\u8fd0\u884c\u3002\r\n\r\n\u63d0\u4ea4\u8981\u6c42\uff1a\r\n\u53ea\u6709\u7b2c\u4e8c\u90e8\u5206\u7684seq-full.hcl\u548cpipe-full.hcl\u987b\u63d0\u4ea4\u5230\u81ea\u52a8\u8bc4\u6d4bhttp://acn.thucloud.com\uff0c\u5176\u4f59\u6253\u5305\u63d0\u4ea4\u7f51\u7edc\u5b66\u5802\uff08\u5305\u62ec\u7b2c\u4e8c\u90e8\u5206\u7684\u6587\u6863\uff09\u3002\u6ce8\u610f\u533a\u5206\u662f\u7b2c\u51e0\u90e8\u5206\u3002\r\n\r\n\u6ce8\u610f\uff1a\r\n\u6587\u6863\u4e2d\u5fc5\u987b\u8981\u6709iaddl\u548cleave\u7684\u8bf4\u660e\uff0c\u4e5f\u5c31\u662f\u8fd9\u4e2a\u6307\u4ee4\u6bcf\u4e2a\u9636\u6bb5\u505a\u4e86\u4ec0\u4e48\u3002",
            "start_time": "2016-11-23",
            "course_name": "\u8ba1\u7b97\u673a\u4e0e\u7f51\u7edc\u4f53\u7cfb\u7ed3\u6784(1)",
            "title": "\u8ba1\u7b97\u673a\u4f53\u7cfb\u7ed3\u6784\u2014\u2014Y86\u5b9e\u9a8c\uff08Architecture\u00a0Lab\uff09",
            "end_time": "2016-12-18"
        }, {
            "detail": "1. \u4e4b\u540e\u4f1a\u5728\u6559\u5b66\u8d44\u6e90\u533a\u4e0a\u4f20TinyOS\u7684Linux\u955c\u50cf\uff0c\u5927\u5bb6\u53ef\u4ee5\u7528\u4e4b\u4ee5\u8282\u7ea6\u914d\u7f6e\u73af\u5883\u7684\u65f6\u95f4\u3002\r\n2. \u672c\u6b21\u5b9e\u9a8c\u7684\u68c0\u67e5\u65e5\u671f\u548c\u63d0\u4ea4\u65e5\u671f\u4e3a\u540c\u4e00\u5929\uff0c\u60f3\u8fd9\u4e00\u5929\u665a\u4e0a\u4ea4\u4f5c\u4e1a\u662f\u884c\u4e0d\u901a\u7684\uff0c\u81f3\u5c11\u8981\u5b8c\u6210\u4e00\u4e2a\u80fd\u5e94\u4ed8\u68c0\u67e5\u7684\u7248\u672c\u3002\r\n",
            "start_time": "2016-11-30",
            "course_name": "\u8ba1\u7b97\u673a\u4e0e\u7f51\u7edc\u4f53\u7cfb\u7ed3\u6784(1)",
            "title": "\u7f51\u7edc\u90e8\u5206\u7b2c\u4e8c\u6b21\u5927\u4f5c\u4e1a\u2014\u2014WSN",
            "end_time": "2016-12-25"
        }, {
            "detail": "",
            "start_time": "2016-11-26",
            "course_name": "\u8ba1\u7b97\u673a\u4e0e\u7f51\u7edc\u4f53\u7cfb\u7ed3\u6784\uff082\uff09",
            "title": "\u7f16\u8bd1\u5c0f\u7ec4\u4f5c\u4e1a",
            "end_time": "2016-12-18"
        }, {
            "detail": "\u5927\u5bb6\u8bb0\u5f97\u6309\u65f6\u5b8c\u6210\u54c8~",
            "start_time": "2016-11-24",
            "course_name": "\u6295\u8d44\u5b66",
            "title": "HW4",
            "end_time": "2016-12-05"
        }, {
            "detail": "",
            "start_time": "2016-12-01",
            "course_name": "\u8ba1\u7b97\u673a\u4e0e\u7f51\u7edc\u4f53\u7cfb\u7ed3\u6784\uff082\uff09",
            "title": "\u7f16\u8bd1\u7b2c\u4e8c\u6b21\u4f5c\u4e1a",
            "end_time": "2016-12-07"
        }]
        return debug # TODO

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
