from django.utils import timezone
from django.shortcuts import render
from codex.baseview import BaseView
from wechat.handlers import *
from wechat.wrapper import WeChatView

class CustomWeChatView(WeChatView):
	handlers = [
		CalculatorHandler,
	]
