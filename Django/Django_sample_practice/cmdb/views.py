from django.shortcuts import render
from django.shortcuts import HttpResponse


def login(request):
    return render(request, 'login.html')
