# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^bind$', UserBind.as_view()),
    url(r'^fortune$', Fortune.as_view()),
]
