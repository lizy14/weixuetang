# -*- coding: utf-8 -*-
#
import json
import logging
from django.http import HttpResponse
from django.views.generic import View
from codex.baseerror import BaseError, InputError, UnbindError


class BaseView(View):

    logger = logging.getLogger('View')

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return self.do_dispatch(*args, **kwargs)

    def do_dispatch(self, *args, **kwargs):
        raise NotImplementedError(
            'You should implement do_dispatch() in sub-class of BaseView')

    def http_method_not_allowed(self, *args, **kwargs):
        return super(BaseView, self).http_method_not_allowed(self.request, *args, **kwargs)
