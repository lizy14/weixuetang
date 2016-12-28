# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^course/?$', List.as_view()),
    url(r'^edit/?$', Edit.as_view()),
    url(r'^delete/?$', Delete.as_view()),
]
