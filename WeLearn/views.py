# -*- coding: utf-8 -*-
#
from codex.baseview import BaseView
from codex.apiview import APIView
from WeLearn import settings
from django.http import HttpResponse, Http404
import logging
import mimetypes
import os


class StaticFileView(BaseView):  # pragma: no cover

    logger = logging.getLogger('Static')

    def get_file(self, fpath):
        if os.path.isfile(fpath):
            return open(fpath, 'rb').read()
        else:
            return None

    def do_dispatch(self, *args, **kwargs):
        if not settings.DEBUG:
            self.logger.warn(
                'Please use nginx/apache to serve static files in production!')
            raise Http404()
        rpath = self.request.path.replace('..', '.').strip('/')
        if '__' in rpath:
            raise Http404(
                'Could not access private static file: ' + self.request.path)
        content = self.get_file(os.path.join(settings.STATIC_ROOT, rpath))
        if content is not None:
            return HttpResponse(content, content_type=mimetypes.guess_type(rpath)[0])
        content = self.get_file(os.path.join(
            settings.STATIC_ROOT, rpath + '/index.html'))
        if content is not None:
            return HttpResponse(content, content_type=mimetypes.guess_type(rpath + '/index.html')[0])
        raise Http404('Could not found static file: ' + self.request.path)

from django.shortcuts import redirect
from urllib.parse import unquote


class RedirectView(APIView):

    def do_dispatch(self, *args, **kwargs):
        self.input = self.query or self.body
        return self.do_redirect()

    @APIView.certificated
    def do_redirect(self):
        if not self.student.xt_id:
            return redirect(settings.get_redirect_url('u/bind'))
        return redirect(settings.get_redirect_url(unquote(self.input['state'])))
