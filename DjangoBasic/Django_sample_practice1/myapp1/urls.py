#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
from django.conf.urls import url,include
from myapp1 import views

urlpatterns = [
    url(r'^orm/', views.orm),
    url(r'^host/', views.host),
    url(r'^ajax_submit/', views.ajax_submit),
    url(r'^ajax_delete/', views.ajax_delete),
    url(r'^edit_submit/', views.edit_submit),
    url(r'^app/', views.app),
    url(r'^app_add_host/', views.app_add_host),

]



