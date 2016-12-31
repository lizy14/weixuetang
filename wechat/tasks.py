from .wrapper import WeChatView
from celery import shared_task
from .models import Template
import logging

__logger__ = logging.getLogger(__name__)

template_name = {
    'new_hw': '您有一个新作业',
    'hw_checked': '您有一个作业被批改了',
    'new_notice': '新学堂公告',
    'new_lec': '新文化素质教育讲座',
}

from WeLearn.settings import get_redirect_url
from datetime import date
from codex.baseerror import OperationError


def wrap_Notice(ins, usr):
    if not usr.pref.s_notice:
        raise OperationError
    return ('new_notice', {
        'course': ins.course.name,
        'title': ins.title,
        'publisher': ins.publisher,
        'content': ins.content,
        'time': ins.publishtime.strftime('%Y-%m-%d'),
    }, get_redirect_url('notice/detail', {
        'notice_id': ins.id
    }))


def wrap_Homework(ins, usr):
    if not usr.pref.s_work:
        raise OperationError
    return ('new_hw', {
        'hw_name': ins.title,
        'course_name': ins.course.name,
        'ddl': ins.end_time.strftime('%Y-%m-%d'),
        'days_left': (ins.end_time - date.today()).days,
    }, get_redirect_url('hw/detail', {
        'homework_id': ins.id
    }))


def wrap_HomeworkStatus(ins, usr):
    if not usr.pref.s_work:
        raise OperationError
    return ('hw_checked', {
        'hw_name': ins.homework.title,
        'course_name': ins.homework.course.name,
        'score': ins.grading,
    }, get_redirect_url('hw/detail', {
        'homework_id': ins.homework.id
    }))


def wrap_Lecture(ins, usr):
    if not usr.pref.s_lecture:
        raise OperationError
    return ('new_lec', {
        'title': ins.title,
        'lecturer': ins.lecturer,
        'time': ins.time,
        'place': ins.place,
    }, get_redirect_url('lecture/detail', {
        'lecture_id': ins.id
    }))


def default_wrapper(data):
    res = {}
    for k, v in data.items():
        res[k] = {
            'value': v,
            'color': '#173177'
        }
    return res


@shared_task
def t_send_template(openid, temp, data, url):
    try:
        WeChatView._wechat.send_template_message(
            openid, WeChatView.get_template_id(template_name[temp]), data, url)
    except Exception as e:
        __logger__.exception(str(e))

from userpage.models import Student
from codex.taskutils import revoke

# NOTE: apply_async_function(task, args=~list or tuple~, kwargs=~dict~,
# **options)


def send_template(openid, ins, spec='', apply_async_function=None, wrapper=None, **options):
    usr = Student.get_by_openid(openid)
    try:
        tup = globals()['wrap_' + ins.__class__.__name__ + spec](ins, usr)
        if not wrapper:
            wrapper = default_wrapper
        t_data = wrapper(tup[1])
        if apply_async_function is None:
            t_send_template.apply_async(
                args=(openid, tup[0], t_data, tup[2]), **options)
        else:
            apply_async_function(t_send_template, (openid, tup[
                                 0], t_data, tup[2]), {}, **options)
    except OperationError:
        return
    except Exception as e:
        __logger__.exception(str(e))


def revoke_send(openid, ins, spec='', wrapper=None, **options):
    usr = Student.get_by_openid(openid)
    try:
        tup = globals()['wrap_' + ins.__class__.__name__ + spec](ins, usr)
        if not wrapper:
            wrapper = default_wrapper
        t_data = wrapper(tup[1])
        revoke(t_send_template, args=(openid, tup[
               0], t_data, tup[2]), kwargs={}, **options)
    except OperationError:
        return
    except Exception as e:
        __logger__.exception(str(e))
