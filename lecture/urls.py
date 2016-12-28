from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^list/?$', List.as_view()),
    url(r'^detail/?$', Detail.as_view()),
]
