#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"


from django import forms
from myapp import models
from django.forms import fields,widgets
from django.forms.models import ModelChoiceField
from django.core.exceptions import ValidationError


class Form1(forms.Form):
    uername = fields.CharField(max_length=32)
    # user_type = fields.ChoiceField(choices=models.UserType.objects.values_list('id', 'name'))
    # user_type2 = fields.CharField(
    #     widget=widgets.Select(choices=models.UserType.objects.values_list('id', 'name'))
    # )

    user_type = fields.ChoiceField(choices=[])
    user_type2 = fields.CharField(
        widget=widgets.Select(choices=[])
    )
    user_type3 = ModelChoiceField(
        queryset=models.UserType.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(Form1, self).__init__(*args, **kwargs)
        self.fields['user_type'].choices = models.UserType.objects.values_list('id', 'name')
        self.fields['user_type2'].widget.choices = models.UserType.objects.values_list('id', 'name')


class LoginForm(forms.Form):

    user = fields.CharField()
    pwd = fields.CharField(validators=[])

    # 1
    def clean_user(self):
        c = models.Users.objects.filter(name=self.cleaned_data['user']).count()
        if not c:
            return self.cleaned_data['user']
        else:
            raise ValidationError('用户名已经存在', code='xxx')

    # 2
    def clean_pwd(self):
        c = models.Users.objects.filter(pwd=self.cleaned_data['pwd']).count()
        if c:
            return self.cleaned_data['pwd']

    # 3
    def clean(self):
        c = models.Users.objects.filter(name=self.cleaned_data['user'], pwd=self.cleaned_data['pwd']).count()
        if c:
            return self.cleaned_data
        else:
            raise ValidationError('用户名或密码错误', code='xxx')
        # {{ obj.errors.__all__ }}
        # obj.errors['__all__']

    # 4
    def _post_clean(self):
        pass
