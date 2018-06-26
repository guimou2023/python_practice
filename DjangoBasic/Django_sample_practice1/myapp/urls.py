#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
from django.conf.urls import url,include
from django.contrib import admin
from myapp import views1
from myapp.businessviews import login

urlpatterns = [
    url(r'^login/', views1.login),
    url(r'^clogin/', views1.clogin),
    url(r'^cindex/', views1.cindex),
    url(r'^slogin/', views1.slogin),
    url(r'^sindex/', views1.sindex),
    url(r'^slogout/', views1.slogout),
    url(r'^orm/', views1.orm),
    url(r'^paging/', views1.paging),
    url(r'^index/', views1.index),
    url(r'^user_info/', views1.user_info),
    url(r'^user_detail-(?P<u_id>\d+)$', views1.user_detail),
    url(r'^user_del-(?P<u_id>\d+)$', views1.user_del),
    url(r'^user_edit-(?P<u_id>\d+)$', views1.user_edit),
    url(r'^testmid/$', views1.tmid),
    url(r'^cache/$', views1.cache),
    url(r'^signal/$', views1.signal),
    url(r'^form/$', views1.form),
    url(r'^form1/$', views1.form1),
    url(r'^model/$', views1.model),
    url(r'^vlogin/$', login.login),
    url(r'^modelform/$', login.modelform),
    url(r'^modelform_userlist/$', login.modelform_userlist),
    url(r'^modelform_useredit-(\d+)/$', login.modelform_useredit),
    url(r'^ajax1/$', login.ajax1),
    url(r'^iframe/$', login.iframe),
    url(r'^file/$', login.file),
    url(r'^preview/$', login.preview),
]