#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse


class M1(MiddlewareMixin):
    def process_request(self, request):
        print('M1 request')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('M1 in view')

    def process_response(self, request, reponse):
        print('M1 response')
        return reponse


class M2(MiddlewareMixin):
    def process_request(self, request):
        print('M2 request')
        # 此处返回，请求不会到达函数
        # return HttpResponse('M2:走')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('M2 in view')

    def process_response(self, request, reponse):
        print('M2 response')
        return reponse


class M3(MiddlewareMixin):
    def process_request(self, request):
        print('M3 request')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('M3 in view')

    def process_response(self, request, reponse):
        print('M3 response')
        return reponse

    def process_exception(self, request, exception):
        if isinstance(exception, ValueError):
            print('M3 exception')
            return HttpResponse('出现异常了！')


# 请求结果：
# M1 request
# M2 request
# M3 request
# M1 in view
# M2 in view
# M3 in view
# M3 exception
# M3 response
# M2 response
# M1 response

