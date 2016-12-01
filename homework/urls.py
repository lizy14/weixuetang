# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^unfinished-list/?$', UnifinishedList.as_view()),
]
