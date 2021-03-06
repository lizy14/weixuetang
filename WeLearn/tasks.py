from django.db import models
from userpage.models import *
from homework.models import *
from notice.models import *
import ztylearn as LearnDAO
import asyncio
from celery import shared_task


@shared_task(name='WeLearn.tasks.main')
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_all())


async def update_all():
    students = Student.objects.filter(xt_id__isnull=False)
    tasks = [
        update_student(i)
        for i in students
    ]
    await asyncio.gather(*tasks)


async def update_student(student):
    xt_id = student.xt_id
    _user = LearnDAO.User(
        username=xt_id
    )
    _semester = LearnDAO.Semester(_user)
    tasks = [
        update_student_course(student, _course)
        for _course in await _semester.courses
    ]
    await asyncio.gather(*tasks)


async def update_student_course(student, _course):
    xt_id = student.xt_id
    course, created = Course.objects.get_or_create(
        xt_id=_course.id,
        name=_course.name
    )
    CourseStatus.objects.get_or_create(
        course=course,
        student=student
    )
    tasks_hw = [
        update_student_course_work(student, course, _homework)
        for _homework in await _course.works
    ]
    tasks_nt = [
        update_student_course_notice(student, course, _notice)
        for _notice in await _course.messages
    ]


def update_student_course_notice(student, course, _notice):
    try:
        notice = Notice.objects.get(
            xt_id=_notice.id,
            course=course,
        )
    except:
        notice = Notice(
            xt_id=_notice.id,
            course=course,
        )
    notice.title = _notice.title
    notice.content = _notice.detail
    notice.publisher = _notice.author
    notice.publishtime = _notice.date
    notice._student = student
    notice.save()


def update_student_course_work(student, course, _homework):
    try:
        homework = Homework.objects.get(
            xt_id=_homework.id,
            course=course,
        )
    except:
        homework = Homework(
            xt_id=_homework.id,
            course=course,
        )
    homework.title = _homework.title
    homework.start_time = _homework.start_time
    homework.end_time = _homework.end_time
    homework.detail = _homework.detail
    homework.attachment = _homework.attachment
    homework._status = _homework
    homework._status.student = student
    homework.save()
