from django.db import models
from userpage.models import *
from homework.models import *

import ztylearn as LearnDAO
import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_all())
# echo "import WeLearn.tasks as t; t.main()" | python manage.py shell


async def notification_hw_new(homeworkStatus):
    _logger.debug("NOTIFICATION %s new homework `%s`" % (
        homeworkStatus.student.xt_id,
        homeworkStatus.homework.title)
    )
    pass

async def notification_hw_graded(homeworkStatus):
    _logger.debug("NOTIFICATION %s homework graded `%s`" % (
        homeworkStatus.student.xt_id,
        homeworkStatus.homework.title)
    )
    pass

async def notification_hw_ddl_modified(homeworkStatus, oldDdl):
    _logger.debug("NOTIFICATION %s homework ddl modified `%s`, %s -> %s" % (
        homeworkStatus.student.xt_id,
        homeworkStatus.homework.title,
        oldDdl,
        homeworkStatus.homework.end_time)
    )
    pass



async def update_all():
    students = Student.objects.all() # TODO
    tasks = [update_student(i) for i in students]
    await asyncio.gather(*tasks)



async def update_student(student):
    xt_id = student.xt_id
    _user = LearnDAO.User(
        username=xt_id
    )
    _semester = LearnDAO.Semester(_user)

    tasks = [update_student_course(student, _course) for _course in await _semester.courses]
    await asyncio.gather(*tasks)



async def update_student_course(student, _course):
    xt_id = student.xt_id
    _logger.debug("Updating Student %s Course %s" % (xt_id, _course.id))
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

    tasks = [update_student_course_work(student, course, _homework) for _homework in await _course.works]
    await asyncio.gather(*tasks)



async def update_student_course_work(student, course, _homework):
    try:
        homework = Homework.objects.get(
            xt_id=_homework.id,
        )

    except Homework.DoesNotExist:
        homework = Homework()
        homework.course     = course
        homework.xt_id      = _homework.id

    ddl_modified = str(homework.end_time) != str(_homework.end_time)
    if ddl_modified:
        old_ddl = homework.end_time

    homework.title      = _homework.title
    homework.start_time = _homework.start_time
    homework.end_time   = _homework.end_time
    homework.detail     = _homework.detail  # CHANGED: remove await
    homework.save()

    newly_created = False
    try:
        homeworkStatus = HomeworkStatus.objects.get(
            student  = student,
            homework = homework
        )
    except HomeworkStatus.DoesNotExist:
        newly_created = True
        homeworkStatus = HomeworkStatus()
        homeworkStatus.student  = student
        homeworkStatus.homework = homework

    graded = _homework.completion > 1
    newly_graded = (not newly_created) and graded and not homeworkStatus.graded

    homeworkStatus.grading   = "" # TODO
    homeworkStatus.graded    = graded
    homeworkStatus.submitted = _homework.completion > 0
    homeworkStatus.save()

    # generate push notifications
    if newly_created:
        await notification_hw_new(homeworkStatus)
    if ddl_modified:
        await notification_hw_ddl_modified(homeworkStatus, old_ddl)
    if newly_graded:
        await notification_hw_graded(homeworkStatus)
