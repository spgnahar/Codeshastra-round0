"""askmeout URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login_blog),
    url(r'^register/$', views.register),
    url(r'^logout/$', views.logout_blog),
    url(r'^ask/', views.ask),
    url(r'^forum/', views.forum),
    url(r'^jargon/', views.jargon),
    url(r'^define/', views.define),
    url(r'^youtube/', views.youtube),
    url(r'^courses/', views.courses),
    url(r'^coursera', views.coursera),
    url(r'^search', views.search),
    url(r'^searcDef' , views.searchDef),
    url(r'^posts/$', views.posts),
    url(r'^new_post/$', views.new_post),
    ####################################
    url(r'^sendAns/(\d+)$', views.sendAns),
    url(r'^sentQues/$', views.sentQues),
    url(r'^questionDetail/(\d+)$', views.questionDetail),
]
