from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views


urlpatterns=[
    path('sign/up/', views.sign_up, name='sign_up'),
    path('login/', views.Login, name='Login'),
    path('Logout',views.Logout,name='Logout'),
    path('',views.HomeView.as_view(), name='home_view'),
    path('forget_password', views.forget_password , name="forget_password"),
    path('reset_password', views.reset_password , name="reset_password"),
    path('update_password', views.update_password , name="update_password"),
]