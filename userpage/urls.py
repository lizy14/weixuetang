# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from userpage.views import *

urlpatterns = [
    url(r'^bind$', UserBind.as_view()),
]
