from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse, render


def t1(request):
    return render(request, 'tem1.html')


def t2(request):
    return render(request, 'tem2.html')


def t3(request):
    return render(request, 'tem3.html')