# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^personal/?$', Personal.as_view()),
    url(r'^global/?$', Global.as_view()),
    url(r'^semester/?$', Semester.as_view()),
]
