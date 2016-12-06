from .wrapper import WeChatView
from celery import shared_task

@shared_task
def t_send_test(openid, tempid, data):
    WeChatView._wechat.send_template_message(openid, tempid, data)
