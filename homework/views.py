from django.shortcuts import render
from userpage.models import *
from .models import *
from codex.baseview import APIView
from codex.baseerror import *

from datetime import datetime
# Create your views here.


class UnifinishedList(APIView):


    def get(self):
        def wrap_homework(hw):
            def wrap_date(d):
                return d.strftime('%Y-%m-%d')
                return datetime.combine(d, datetime.min.time()).timestamp()
            return {
                'start_time' : wrap_date(hw.start_time),
                'end_time'   : wrap_date(hw.end_time),
                'title'      : hw.title,
                'course_name': hw.course.name
            }


        self.check_input('student_id', 'token')
        xt_id = self.input['student_id']
        token = self.input['token']

        student = Student.objects.get(xt_id=xt_id)
        if token != student.token:
            return []

        result = []
        for hwStatus in HomeworkStatus.objects.filter(student__id=student.id):
            if not hwStatus.submitted:
                result.append(wrap_homework(hwStatus.homework))
        return result
