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
from .models import Template

# !IMPORTENT
# HANDLERS ONLY
# DO NOT DEFINE ANY OTHER CLASSES
# WITH SUFFIX 'Handler'


class CalculatorHandler(WeChatHandler):

    def check(self):
        return self.msg_type_is('text') and re.match(r'^[0-9\+\-\*\/\(\)]+$', self.msg.content) is not None

    def handle(self):
        try:
            res = eval(self.msg.content)
        except:
            res = 'Kind of unresolvable expression.'
        return self.wechat.response_text(content=str(res))


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

from userpage.tasks import notify


class TemplateHandler(WeChatHandler):

    def check(self):
        return self.is_event_of('templatesendjobfinish')

    def handle(self):
        if self.msg.status == 'success':
            return
        else:
            self.__logger__.critical(self.msg.status)
            raise OperationError(self.msg.status)


class MenuHandler(WeChatHandler):

    def check(self):
        return self.msg_type_is('view')

    def handle(self):
        pass


class SubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_event_of('subscribe')

    def handle(self):
        return self.wechat.response_text(content='Welcome~ : )')
