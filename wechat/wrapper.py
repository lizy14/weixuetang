# -*- coding: utf-8 -*-
#
from codex.baseview import BaseView
from django.http import Http404, HttpResponse
from django.template.loader import get_template
import logging
from wechat_sdk import WechatBasic
from WeLearn.settings import wechat_conf
from userpage.models import Student
from .models import Template
from wechat_sdk.messages import *


class WeChatHandler(object):
    """ Base handler class"""

    def __init__(self, view, user):
        self.context = view
        self.user = user
        self.wechat = self.context.wechat
        self.msg = self.wechat.message

    def check(self):
        raise NotImplementedError('WeChatHandler:check() not implemented!')

    def handle(self):
        raise NotImplementedError('WeChatHandler:handle() not implemented!')

    def msg_type_is(self, typ):
        return self.msg.type == typ

    def is_text(self, *args):
        return self.msg_type_is('text') and (self.msg.content.lower() in args)

    def is_click_of_event(self, eve):
        return self.msg.type == 'click' and self.msg.key == self.context.event_keys[eve]

    def is_event_of(self, *events):
        return isinstance(self.msg, EventMessage) and self.msg.type in events


class WeChatEmptyHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.wechat.response_text(content='Server Error.. Please contact the administrator!')


class WeChatView(BaseView):

    logger = logging.getLogger('WeChat')
    handlers = []
    _wechat = WechatBasic(conf=wechat_conf)
    error_message_handler = WeChatEmptyHandler
    default_handler = WeChatEmptyHandler

    @property
    def wechat(self):
        return self._wechat

    @classmethod
    def get_template_id(cls, name):
        return Template.get_template_id(name)

    @classmethod
    def open_id_from_code(cls, code):
        resp = cls._wechat.request.get(
            url='https://api.weixin.qq.com/sns/oauth2/access_token',
            params={
                "grant_type": "authorization_code",
                "appid": cls._wechat.conf.appid,
                "secret": cls._wechat.conf.appsecret,
                "code": code,
            })
        return resp['openid']

    def _check_signature(self):
        query = self.request.GET
        return self.wechat.check_signature(signature=query['signature'], timestamp=query['timestamp'], nonce=query['nonce'])

    def do_dispatch(self, *args, **kwargs):
        if not self._check_signature():
            self.logger.error(
                'WeChatView:do_dispatch() check signature failed!')
            return Http404()
        if self.request.method == 'GET':
            return HttpResponse(self.request.GET['echostr'])
        elif self.request.method == 'POST':
            return HttpResponse(self.handle_wechat_msg(), content_type='application/xml')
        else:
            return self.http_method_not_allowed()

    def handle_wechat_msg(self):
        try:
            self.wechat.parse_data(self.request.body)
        except Exception as e:
            self.logger.error('WeChatView:handle_wechat_msg() parse error')
            return self.error_message_handler(self, None).handle()
        user, created = Student.objects.get_or_create(
            open_id=self.wechat.message.source)
        if created:
            self.logger.info('New user: {}'.format(user.open_id))
        try:
            for handler in self.handlers:
                inst = handler(self, user)
                if inst.check():
                    return inst.handle()
            return self.default_handler(self, user).handle()
        except:
            self.logger.exception('Error occurred when handling WeChat message {}'.format(
                self.wechat.message.raw))
            return self.error_message_handler(self, user).handle()
