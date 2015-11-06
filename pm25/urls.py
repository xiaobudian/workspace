#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getweather/(?P<code>[0-9]+)/$', views.getweather, name='getweather'),
    url(r'^updateprovince$', views.updateprovince, name='updateprovince'),
    url(r'^updatecity$', views.updatecity, name="updatecity"),
    url(r'^updatetown$', views.updatetown, name="updatetown"),
    url(r'^getareaxml$', views.getareaxml, name="getareaxml"),
]
