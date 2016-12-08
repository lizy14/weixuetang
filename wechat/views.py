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
    event_keys = {
        'news_assignments': 'NEWS_ASI',
        'news_broadcasts': 'NEWS_BRO',
        'news_lectures': 'NEWS_LEC',
        'calendar': 'CALEN',
        'info_bind': 'INFO_BIN',
        'info_SETTING': 'INFO_SET',
        'info_test': 'INFO_TEST',
    }
    menu = {
        'button': [
            {
                'name': '新鲜事',
                'sub_button': [
                    {
                            'type': 'view',
                            'name': '作业',
                            'url': get_redirect_url('hw/unfinished-list'),
                        },
                    {
                            'type': 'view',
                            'name': '公告',
                            'url': get_redirect_url('notice/list'),
                        },
                    {
                            'type': 'click',
                            'name': '讲座',
                            'key': event_keys['news_lectures'],
                        }
                ]
            },
            {
                'type': 'click',
                'name': '日历',
                'key': event_keys['calendar']
            },
            {
                'name': '个人中心',
                'sub_button': [
                        {
                            'type': 'view',
                            'name': '绑定/解绑',
                            'url': get_redirect_url('u/bind'),
                        },
                    {
                            'type': 'click',
                            'name': '设置',
                                    'key': event_keys['info_SETTING'],
                    },
                    {
                            'type': 'click',
                            'name': '测试',
                                    'key': event_keys['info_test'],
                    }
                ]
            }
        ]
    }

    @classmethod
    def update_menu(cls, menu=None):
        if not menu:
            menu = cls.menu
        try:
            cls._wechat.create_menu(menu)
        except Exception as e:
            raise BaseError(-1,
                            'CustomWeChatView:update_menu() error setting menu: {}'.format(str(e)))

    @classmethod
    def get_templates(cls):
        Template.objects.all().delete()
        res = cls._wechat.request.get(
            url='https://api.weixin.qq.com/cgi-bin/template/get_all_private_template')
        ls = res['template_list']
        for item in ls:
            dat = Template(t_id=item['template_id'], t_title=item['title'])
            dat.save()
            logger.info('Saved {} with {}.'.format(dat.t_title, dat.t_id))
