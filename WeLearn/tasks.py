from django.db import models
from userpage.models import *
from homework.models import *
import aiolearn

import asyncio

async def update_all():
    students = Student.objects.filter() #TODO
    tasks = [update_student(i) for i in students]
    await asyncio.gather(*tasks)


async def update_student(student):
    _user = aiolearn.User(
        username=student.xt_id,
        password=student.xt_pw
    )
    _semester = aiolearn.Semester(_user, current=True)

    for _course in await _semester.courses: # TODO: parallize
        course, created = Course.objects.get_or_create(
            xt_id=_course.id
        )
        if created:
            course.name = _course.name
            course.save()
        CourseStatus.objects.get_or_create(
            course_id  = course.id,
            student_id = student.id
        )

        for _homework in await _course.works:
            homework, created = Homework.objects.get_or_create(
                xt_id=_homework.id
            )
            if created:
                homework.title      = _homework.title
                homework.start_time = _homework.start_time
                homework.end_time   = _homework.end_time
                homework.detail     = _homework.detail
                homework.save()

            homeworkStatus, created = HomeworkStatus.objects.get_or_create(
                student__id  = student.id,
                homework__id = homework.id
            )
            if created:
                send_new_homework_notification(homeworkStatus)

            homeworkStatus.graded = False # TODO
            homeworkStatus.grading = ""
            homeworkStatus.submitted = _homework.completion # TODO
            homeworkStatus.save()



async def send_new_homework_notification(homeworkStatus):
    pass
