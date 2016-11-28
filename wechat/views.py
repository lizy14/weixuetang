# -*- coding: utf-8 -*-
#
from django.utils import timezone
from django.shortcuts import render
from codex.baseview import BaseView
from wechat import handlers as handlers_module
from wechat.handlers import *
from wechat.wrapper import WeChatView
import inspect

class CustomWeChatView(WeChatView):
	handlers = [eval(m[0]) for m in inspect.getmembers(handlers_module, inspect.isclass) if m[1].__module__ == handlers_module.__name__]
	event_keys = {
		'news_all': 'NEWS_ALL',
		'news_assignments': 'NEWS_ASI',
		'news_broadcasts': 'NEWS_BRO',
		'news_lectures': 'NEWS_LEC',
		'talk_teacher': 'TALK_TEA',
		'talk_discuss': 'TALK_DIS',
		'info_bind': 'INFO_BIN',
		'info_SETTING': 'INFO_SET',
	}
	menu = {
		'button': [
			{
				'name': '新鲜事',
				'sub_button': [
					{
						'type': 'click',
						'name': '全部',
						'key': event_keys['news_all'],
					},
					{
						'type': 'click',
						'name': '作业',
						'key': event_keys['news_assignments'],
					},
					{
						'type': 'click',
						'name': '公告',
						'key': event_keys['news_broadcasts'],
					},
					{
						'type': 'click',
						'name': '讲座',
						'key': event_keys['news_lectures'],
					}
				]
			},
			{
				'name': '说两句',
				'sub_button': [
					{
						'type': 'click',
						'name': '找老师',
						'key': event_keys['talk_teacher'],
					},
					{
						'type': 'click',
						'name': '发讨论',
						'key': event_keys['talk_discuss'],
					}
				]
			},
			{
				'name': '个人中心',
				'sub_button': [
					{
						'type': 'click',
						'name': '绑定信息',
						'key': event_keys['info_bind'],
					},
					{
						'type': 'click',
						'name': '设置',
						'key': event_keys['info_SETTING'],
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
		except:
			raise BaseError(-1, 'CustomWeChatView:update_menu() error setting menu!')
