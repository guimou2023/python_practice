#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"

from django.shortcuts import render, HttpResponse
from django import forms
from django.forms import fields,widgets
from django.forms.models import ModelChoiceField
from django.core.exceptions import ValidationError



class LoginForm(forms.Form):
    user = fields.CharField()
    pwd = fields.CharField(
        max_length=12,
        min_length=5,
    )

import json

import json
from datetime import date
from datetime import datetime
from django.core.exceptions import ValidationError


class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):

        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        elif isinstance(field, ValidationError):
            return {'code': field.code, 'messages': field.messages}
        else:
            return json.JSONEncoder.default(self, field)


def login(request):
    res = {'status': True, 'errors': None, 'data': None}
    if request.method == "GET":
        return render(request, 'vlogin.html')
    elif request.method == "POST":
        obj = LoginForm(request.POST)
        if obj.is_valid():
            # print(obj.cleaned_data)
            res['data'] = obj.cleaned_data
        else:
            # 字符串类型
            print(obj.errors.as_json(), '的type:', type(obj.errors.as_json()))
            # 字典类型
            print(obj.errors.as_data(), '的type:', type(obj.errors.as_data()))
            # res['errors'] = obj.errors.as_json()
            res['errors'] = obj.errors.as_data()
    # res = json.dumps(res)
    res = json.dumps(res, cls=JsonCustomEncoder)
    print(res)
    return HttpResponse(res)


# modelForm练习
from myapp import models

class UserForm(forms.Form):
    user = fields.CharField()
    email = fields.CharField(
        max_length=12,
        min_length=5,
    )
    user_type = fields.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].choices = models.UserType.objects.values_list('id', 'name')

from django.forms import widgets as Fwidgets
from django.forms import fields as Ffields
class UserModelForm(forms.ModelForm):

    is_rem = Ffields.CharField(
        widget=Fwidgets.CheckboxInput()
    )
    class Meta:
        model = models.Fstaff
        fields = '__all__'
        # fields = ['username', 'email']
        # exclude = ['username']
        labels = {
            'username': '用户名',
            'password': '密码',
        }
        help_texts = {
            'username': '这里写用户名哦'
        }
        widgets = {
            'username': Fwidgets.Textarea(attrs={'class': 'c1'})
        }
        error_messages = {
            # 定义整体错误信息
            '__all__': {},
            # 定义单个字段错误信息
            'email': {
                'required': '邮箱不能为空',
                'invalid': '格式错误',
            }
        }
        field_classes = {
            'email': Ffields.URLField
        }

    def clean_staff_name(self):
        old = self.cleaned_data['staff_name']
        pass
        return old


def modelform(request):
    if request.method == "GET":
        obj = UserModelForm()
        return render(request, 'modelform.html', {'obj': obj})
    elif request.method == "POST":
        obj = UserModelForm(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)
            # obj.save() # 与下三行意义相同，只是拆分开实现
            instance = obj.save(commit=False)
            instance.save()
            obj.save_m2m()
        else:
            print(obj.errors.as_json)
        return render(request, 'modelform.html', {'obj': obj})


def modelform_userlist(request):
    mo_obj_list = models.Fstaff.objects.all().select_related('staff_type')
    print(mo_obj_list)
    return render(request, 'modelform_userlist.html', {'mo_obj_list': mo_obj_list})


def modelform_useredit(request, u_id):
    staff_obj = models.Fstaff.objects.filter(id=u_id).first()
    if request.method == "GET":
        mo_obj = UserModelForm(instance=staff_obj)
    elif request.method == "POST":
        print(staff_obj.gender, 'before')
        mo_obj = UserModelForm(request.POST, instance=staff_obj)
        if mo_obj.is_valid():
            mo_obj.save()
            print(staff_obj.gender, 'after')
        else:
            print(mo_obj.errors.as_json)
    return render(request, 'modelform_useredit.html', {'mo_obj': mo_obj, 'u_id': u_id})



# ajax练习
import json
def ajax1(request):
    res = {'code':None, 'data':None}
    if request.method == "GET":
        print(request.GET)
        return render(request, 'ajax1.html')
    elif request.method == "POST":
        print(request.POST)
        # return HttpResponse('OK', status=404, reason='not found.')

        return HttpResponse(json.dumps(res))

import json
def iframe(request):
    if request.method == "GET":
        return render(request, 'iframe.html')
    elif request.method == "POST":
        print('post 请求来啦。')
        res = {'user': None, 'pwd': None}
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        res.update({'user': user})
        res.update({'pwd': pwd})
        print(res)

        return HttpResponse(json.dumps(res))


def file(request):
    if request.method == "GET":
        return render(request, 'file.html')

    elif request.method == "POST":
        print('FILES', request.FILES)
        file_obj = request.FILES.get("fname")
        print('file_obj_name:', file_obj, 'obj_name:{}'.format(file_obj.name), type(file_obj))
        import os
        file_path = os.path.join('upload/',file_obj.name)
        res = {'file_path': file_path, 'uploaded': True}
        f = open(file_path, 'wb')
        for i in file_obj.chunks():
            f.write(i)
        f.close()
        return HttpResponse(json.dumps(res))


import os
def preview(request):
    if request.method == "GET":
        # print(os.getcwd())
        return render(request, 'preview.html')
    elif request.method == "POST":
        file_obj = request.FILES.get("fname")
        file_path = os.path.join('static/img', file_obj.name)
        print('file_path', file_path)
        res = {'file_path': file_path, 'uploaded': True}
        with open(file_path, 'wb') as f:
            for i in file_obj.chunks():
                f.write(i)
        return HttpResponse(json.dumps(res))