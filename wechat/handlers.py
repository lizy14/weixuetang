# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
import re
from django.utils import timezone
from codex.baseerror import *
import datetime
import pytz
from WeLearn import settings
from celery import shared_task
from wechat.tasks import t_send_test
from .models import Template

# !IMPORTENT
# HANDLERS ONLY
# DO NOT DEFINE ANY OTHER CLASSES
# WITH SUFFIX 'Handler'

template_name = {
    'new_hw': '您有一个新作业',
    'ddl_changed': '作业DDL有变化',
    'hw_checked': '您有一个作业被批改了'
}

class CalculatorHandler(WeChatHandler):

    def check(self):
        return self.msg_type_is('text') and re.match(r'^[0-9\+\-\*\/\(\)]+$', self.msg.content) is not None

    def handle(self):
        try:
            res = eval(self.msg.content)
        except:
            res = 'Kind of unresolvable expression.'
        return self.wechat.response_text(content=str(res))


class BindStudentHandler(WeChatHandler):
    res_bind = '您还没有绑定\n\n<a href="{}">点此绑定</a>'
    res_unbind = '您已经绑定学号:\n{}\n\n回复“解绑”解除绑定'

    def check(self):
        return self.is_click_of_event('info_bind')

    def handle(self):
        if self.user.xt_id is not None:
            return self.wechat.response_text(content=self.res_unbind.format(self.user.xt_id))
        else:
        	return self.wechat.response_text(content=self.res_bind.format(settings.get_url('u/bind', {
                'openid': self.user.open_id
            })))

class UnBindStudentHandler(WeChatHandler):
    response = '解绑成功\n\n<a href="{}">点此重新绑定</a>'

    def check(self):
        return self.is_text('解绑')

    def handle(self):
        self.user.xt_id = None
        self.user.save()
        return self.wechat.response_text(content=self.response.format(settings.get_url('u/bind', {
            'openid': self.user.open_id
        })))

class TestHandler(WeChatHandler):

    def check(self):
        return self.is_click_of_event('info_test')

    def handle(self):
        t_send_test.delay(self.user.open_id, Template.get_template_id(template_name['new_hw']), {
            'hw_name': {
                'value': '作业名',
            },
            'course_name': {
                'value': '软件工程(3)',
            },
            'days_left': {
                'value': '233',
            },
            'ddl': {
                'value': datetime.datetime.now().isoformat(),
            }
        })
        return self.wechat.response_text(content='Done')
