from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from .views import home, contact_us

urlpatterns = [
    path('', home, name='home'),
    path('contactus', contact_us, name='contactus'),

]
