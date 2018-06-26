#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"

from django import template

register = template.Library()


@register.filter
def my_filter(v1, v2):
    return v1 + v2


