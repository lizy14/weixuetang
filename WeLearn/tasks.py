from django.db import models
from userpage.models import *
from homework.models import *
from notice.models import *
from datetime import date
import ztylearn as LearnDAO
import asyncio
from celery import shared_task
from wechat.tasks import send_template
import logging
from .settings import get_redirect_url

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


@shared_task(name='WeLearn.tasks.main')
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_all())


async def notification_notice_new(noticeStatus):
    _logger.debug("NOTIFICATION %s new notice `%s` for course `%s`" % (
        noticeStatus.student.xt_id,
        noticeStatus.notice.title,
        noticeStatus.notice.course.name)
    )
    notice = noticeStatus.notice
    send_template(noticeStatus.student.open_id, 'new_notice', {
        'course': notice.course.name,
        'title': notice.title,
        'publisher': notice.publisher,
        'content': notice.content,
        'time': notice.publishtime.strftime('%Y-%m-%d'),
    }, get_redirect_url('notice/detail', {
        'notice_id': notice.id
    }))


async def notification_hw_new(homeworkStatus):
    _logger.debug("NOTIFICATION %s new homework `%s`" % (
        homeworkStatus.student.xt_id,
        homeworkStatus.homework.title)
    )
    hw = homeworkStatus.homework
    send_template(homeworkStatus.student.open_id, 'new_hw', {
        'hw_name': hw.title,
        'course_name': hw.course.name,
        'ddl': hw.end_time.strftime('%Y-%m-%d'),
        'days_left': (hw.end_time - date.today()).days
    }, get_redirect_url('hw/detail', {
        'homework_id': hw.id
    }))

async def notification_hw_graded(homeworkStatus):
    _logger.debug("NOTIFICATION %s homework graded `%s`" % (
        homeworkStatus.student.xt_id,
        homeworkStatus.homework.title)
    )
    hw = homeworkStatus.homework
    send_template(homeworkStatus.student.open_id, 'hw_checked', {
        'hw_name': hw.title,
        'course_name': hw.course.name,
        'score': homeworkStatus.grading
    }, get_redirect_url('hw/detail', {
        'homework_id': hw.id
    }))

async def notification_hw_ddl_modified(homeworkStatus, oldDdl):
    _logger.debug("NOTIFICATION %s homework ddl modified `%s`, %s -> %s" % (
        homeworkStatus.student.xt_id,
        homeworkStatus.homework.title,
        oldDdl,
        homeworkStatus.homework.end_time)
    )
    hw = homeworkStatus.homework
    send_template(homeworkStatus.student.open_id, 'ddl_changed', {
        'hw_name': hw.title,
        'course_name': hw.course.name,
        'ddl': hw.end_time.strftime('%Y-%m-%d'),
        'days_left': (hw.end_time - date.today()).days
    }, get_redirect_url('hw/detail', {
        'homework_id': hw.id
    }))


async def update_all():
    students = Student.objects.all()  # TODO
    tasks = [update_student(i) for i in students]
    await asyncio.gather(*tasks)


async def update_student(student, mute=False):
    xt_id = student.xt_id
    _user = LearnDAO.User(
        username=xt_id
    )
    _semester = LearnDAO.Semester(_user)

    tasks = [
        update_student_course(student, _course, mute)
        for _course in await _semester.courses
    ]
    await asyncio.gather(*tasks)


async def update_student_course(student, _course, mute):
    xt_id = student.xt_id
    _logger.debug("Updating Student %s Course %s" % (xt_id, _course.id))
    course, created = Course.objects.get_or_create(
        xt_id=_course.id
    )
    if created:
        course.name = _course.name
        course.save()
    CourseStatus.objects.get_or_create(
        course_id=course.id,
        student_id=student.id
    )

    tasks = [
        update_student_course_work(student, course, _homework, mute)
        for _homework in await _course.works
    ]
    await asyncio.gather(*tasks)

    for _notice in await _course.messages:
        await update_student_course_notice(student, course, _notice, mute)


async def update_student_course_notice(student, course, _notice, mute):

    # Notice
    try:
        notice = Notice.objects.get(
            xt_id=_notice.id,
            course__id=course.id
        )
        # TODO detect changes
    except Notice.DoesNotExist:
        notice = Notice()
        notice.course = course
        notice.xt_id = _notice.id

    notice.title = _notice.title
    notice.content = _notice.detail
    notice.publisher = _notice.author
    notice.publishtime = _notice.date
    notice.save()

    # NoticeStatus
    newly_created = False
    try:
        noticeStatus = NoticeStatus.objects.get(
            student=student,
            notice=notice
        )
    except NoticeStatus.DoesNotExist:
        newly_created = True if not mute else False
        noticeStatus = NoticeStatus()
        noticeStatus.student = student
        noticeStatus.notice = notice
        noticeStatus.read = False  # TODO
        noticeStatus.save()

    if newly_created:
        await notification_notice_new(noticeStatus)


async def update_student_course_work(student, course, _homework, mute):

    try:
        homework = Homework.objects.get(
            xt_id=_homework.id,
        )

    except Homework.DoesNotExist:
        homework = Homework()
        homework.course = course
        homework.xt_id = _homework.id

    ddl_modified = str(homework.end_time) != str(_homework.end_time)
    if ddl_modified:
        old_ddl = homework.end_time

    homework.title = _homework.title
    homework.start_time = _homework.start_time
    homework.end_time   = _homework.end_time
    homework.detail     = _homework.detail
    homework.attachment = _homework.attachment
    homework.save()

    newly_created = False
    try:
        homeworkStatus = HomeworkStatus.objects.get(
            student=student,
            homework=homework
        )
    except HomeworkStatus.DoesNotExist:
        newly_created = True if not mute else False
        homeworkStatus = HomeworkStatus()
        homeworkStatus.student = student
        homeworkStatus.homework = homework

    graded = _homework.completion > 1
    newly_graded = (not mute) and (not newly_created) and graded and not homeworkStatus.graded

    homeworkStatus.graded    = graded if not mute else False
    homeworkStatus.grading   = _homework.grading
    homeworkStatus.grading_comment = _homework.grading_comment
    homeworkStatus.graded_by = _homework.grading_author
    homeworkStatus.submitted = _homework.completion > 0
    homeworkStatus.save()

    # generate push notifications
    if newly_created:
        await notification_hw_new(homeworkStatus)
    elif ddl_modified:
        await notification_hw_ddl_modified(homeworkStatus, old_ddl)
    if newly_graded:
        await notification_hw_graded(homeworkStatus)
