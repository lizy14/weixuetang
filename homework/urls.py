# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^unfinished-list/?$', UnfinishedList.as_view()),
    url(r'^list/?$', List.as_view()),
    url(r'^detail/?$', Detail.as_view()),
    url(r'^mark/?$', Mark.as_view()),
]
