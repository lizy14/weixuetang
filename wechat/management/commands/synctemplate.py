# -*- coding: utf-8 -*-
#
import logging
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from wechat.views import CustomWeChatView


class Command(BaseCommand):
    help = 'Synchronize WeChat templates'
    logger = logging.getLogger('synctemplate')

    def handle(self, *args, **options):
        CustomWeChatView.get_templates()
        self.logger.info('Updated templates.')

Command.logger.setLevel(logging.DEBUG)
