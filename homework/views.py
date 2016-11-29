from django.shortcuts import render
from userpage.models import Student, HomeworkStatus, Homework
# Create your views here.

class UnifinishedList(APIView):
    def wrap_homework(hw):
        return {
            'start_time' : hw.start_time,
            'end_time'   : hw.end_time,
            'title'      : hw.title,
            'course_name': hw.course.name
        }
    def get(self):
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
