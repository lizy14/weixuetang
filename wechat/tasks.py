from .views import CustomWeChatView
from celery import shared_task

@shared_task
def t_send_test(word):
    
