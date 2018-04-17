"""Django_sample_practice1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from myapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login', views.login),
    url(r'^Login', views.Login.as_view()),
    url(r'^index$', views.index),
    url(r'^index1$', views.index1),
    url(r'^detail$', views.detail),
    url(r'^detail1-(\d+)$', views.detail1),
    url(r'^detail1-(\d+)-(\d+)$', views.detail2),
    url(r'^detail1-(?P<h1>\d+)-(?P<h2>\d+)-(?P<h3>\d+)$', views.detail3),
    url(r'^myapp/', include("myapp.urls")),

]
