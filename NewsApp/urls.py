from django.contrib import admin
from django.urls import path, include

from NewsApp import views

urlpatterns = [
    path('', views.helloworld),
]
