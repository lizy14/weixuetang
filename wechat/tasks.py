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
        __logger__.exception(e.__str__)


def send_template(openid, temp, data, url='', wrapper=None):
    if not wrapper:
        wrapper = default_wrapper
    t_data = wrapper(data)
    t_send_template.delay(openid, temp, t_data, url)
