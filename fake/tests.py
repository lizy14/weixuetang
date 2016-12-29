# -*- coding: utf-8 -*-
#
from codex.basetest import BaseTest
from .views import *
import logging
__logger__ = logging.getLogger(name=__name__)


class FakeTest(BaseTest):

    def test_newhw(self):
        resp = self.simulate('post', '/api/fake/newhw/', {
            'title': '这里是标题'
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)
