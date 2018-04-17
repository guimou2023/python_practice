#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
from django.conf.urls import url,include
from django.contrib import admin
from myapp import views1

urlpatterns = [
    url(r'^login/', views1.login),
    url(r'^orm/', views1.orm),
    url(r'^index/', views1.index),
    url(r'^user_info/', views1.user_info),
    url(r'^user_detail-(?P<u_id>\d+)$', views1.user_detail),
    url(r'^user_del-(?P<u_id>\d+)$', views1.user_del),
    url(r'^user_edit-(?P<u_id>\d+)$', views1.user_edit),
]