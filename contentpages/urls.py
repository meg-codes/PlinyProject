from django.conf.urls import url

from .views import ContentPage

urlpatterns = [
    url(r'^(?P<template>\w+)/$', ContentPage.as_view(), name='render')
]