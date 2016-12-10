from .wrapper import WeChatView
from celery import shared_task
from .models import Template
import logging

__logger__ = logging.getLogger(__name__)

template_name = {
    'new_hw': '您有一个新作业',
    'ddl_changed': '作业DDL有变化',
    'hw_checked': '您有一个作业被批改了',
    'new_notice': '新学堂公告',
}

from WeLearn.settings import get_redirect_url
from datetime import date

def wrap_Notice(ins):
    return ('new_notice', {
        'course': ins.course.name,
        'title': ins.title,
        'publisher': ins.publisher,
        'content': ins.content,
        'time': ins.publishtime.strftime('%Y-%m-%d'),
    }, get_redirect_url('notice/detail', {
        'notice_id': ins.id
    }))

def wrap_Homework(ins):
    return ('new_hw', {
        'hw_name': ins.title,
        'course_name': ins.course.name,
        'ddl': ins.end_time.strftime('%Y-%m-%d'),
        'days_left': (ins.end_time - date.today()).days,
    }, get_redirect_url('hw/detail', {
        'homework_id': ins.id
    }))

def wrap_Homeworkddl(ins):
    tup = wrap_Homework(ins)
    tup[0] = 'ddl_changed'
    return tup

def wrap_Homeworkchecked(ins):
    return ('hw_checked', {
        'hw_name': ins.title,
        'course_name': ins.course.name,
        'score': ins.status.grading,
    }, get_redirect_url('hw/detail', {
        'homework_id': ins.id
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


def send_template(openid, ins, spec='', wrapper=None):
    try:
        tup = eval('wrap_' + ins.__class__.__name__ + spec + '(ins)')
    except Exception as e:
        __logger__.exception(str(e))
        return
    if not wrapper:
        wrapper = default_wrapper
    t_data = wrapper(tup[1])
    t_send_template.delay(openid, tup[0], t_data, tup[2])
