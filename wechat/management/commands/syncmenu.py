# -*- coding: utf-8 -*-
#
import logging
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from wechat.views import CustomWeChatView


class Command(BaseCommand):
    help = 'Synchronize WeChat menu'
    logger = logging.getLogger('syncmenu')

    def handle(self, *args, **options):
        CustomWeChatView.update_menu()
        self.logger.info('Updated menu.')

Command.logger.setLevel(logging.DEBUG)
