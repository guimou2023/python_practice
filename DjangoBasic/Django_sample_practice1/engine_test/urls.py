#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"

from django.conf.urls import url
from engine_test import views


urlpatterns = [
    url(r'^1/', views.t1),
    url(r'^2/', views.t2),
    url(r'^3/', views.t3),
]