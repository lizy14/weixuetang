"""WeLearn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from wechat.views import CustomWeChatView
from WeLearn.views import StaticFileView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^wechat/?$', CustomWeChatView.as_view()),
    url(r'^api/u/', include('userpage.urls')),
    url(r'^api/hw/', include('homework.urls')),
    url(r'^api/notice/', include('notice.urls')),
    url(r'^api/cal/', include('calendar_.urls')),
    url(r'^api/team/', include('team.urls')),
    url(r'^api/lecture/', include('lecture.urls')),
    url(r'^', StaticFileView.as_view()),
]
