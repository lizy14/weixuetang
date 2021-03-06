# -*- coding: utf-8 -*-
#
from django.utils import timezone
from django.shortcuts import render
from codex.baseview import BaseView
from wechat import handlers as handlers_module
from wechat.handlers import *
from wechat.wrapper import WeChatView
import inspect
from .models import Template
import logging
from WeLearn.settings import get_redirect_url

logger = logging.getLogger(name=__name__)


class CustomWeChatView(WeChatView):
    handlers = [eval(m[0]) for m in inspect.getmembers(
        handlers_module, inspect.isclass) if m[1].__module__ == handlers_module.__name__ and m[1].__name__.endswith('Handler')]
    event_keys = {}
    menu = {
        'button': [
            {
                'name': '新鲜事',
                'sub_button': [
                    {
                        'type': 'view',
                        'name': '作业',
                        'url': get_redirect_url('redirect', state='hw/unfinished-list'),
                    },
                    {
                        'type': 'view',
                        'name': '公告',
                        'url': get_redirect_url('redirect', state='notice/list'),
                    },
                    {
                        'type': 'view',
                        'name': '日历',
                        'url': get_redirect_url('redirect', state='calendar'),
                    }
                ]
            },
            {
                'name': '发现',
                'sub_button': [
                    {
                        'type': 'view',
                        'name': '讲座',
                        'url': get_redirect_url('redirect', state='lecture/list'),
                    },
                    {
                        'type': 'view',
                        'name': '组队',
                        'url': get_redirect_url('redirect', state='team'),
                    }
                ]
            },
            {
                'name': '个人中心',
                'sub_button': [
                        {
                            'type': 'view',
                            'name': '绑定/解绑',
                            'url': get_redirect_url('redirect', state='u/bind'),
                        },
                    {
                            'type': 'view',
                            'name': '偏好设置',
                            'url': get_redirect_url('redirect', state='u/pref'),
                    }
                ]
            }
        ]
    }

    @classmethod
    def update_menu(cls, menu=None):  # pragma: no cover
        if not menu:
            menu = cls.menu
        try:
            cls._wechat.create_menu(menu)
        except Exception as e:
            raise BaseError(-1,
                            'CustomWeChatView:update_menu() error setting menu: {}'.format(str(e)))

    @classmethod
    def get_templates(cls):  # pragma: no cover
        Template.objects.all().delete()
        res = cls._wechat.request.get(
            url='https://api.weixin.qq.com/cgi-bin/template/get_all_private_template')
        ls = res['template_list']
        for item in ls:
            dat = Template(t_id=item['template_id'], t_title=item['title'])
            dat.save()
            logger.info('Saved {} with {}.'.format(dat.t_title, dat.t_id))
