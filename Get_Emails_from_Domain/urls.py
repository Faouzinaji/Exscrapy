from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views


urlpatterns=[






#urls for the domain get data
path('get_email_from_domain', views.get_email_from_domain, name='get_email_from_domain'),
path('get_data_email_from_domain', views.get_data_email_from_domain, name='get_data_email_from_domain'),
path('pay_as_go_get_email_from_domain/<int:expected_price>', views.pay_as_go_get_email_from_domain, name='pay_as_go_get_email_from_domain'),
path('pay_as_go_get_email_from_domain_success', views.pay_as_go_get_email_from_domain_success, name='pay_as_go_get_email_from_domain_success'),



]