from django.contrib import admin
from django.urls import path, include

from NewsApp import views

urlpatterns = [
    path('', views.news, name='index'),
    path('auth/', views.authForm, name='auth'),
    path('auth/signin', views.authSignIn),
    path('auth/signup', views.authSignUp),
    path('auth/logout', views.authSignOut, name='signout'),
    path('news/', views.news),
]
