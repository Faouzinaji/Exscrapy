from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views


urlpatterns=[



path('index/', views.index, name='index'),
path('get_data_option', views.get_data_option, name='get_data_option'),
path('getdata', views.getdata, name='getdata'),
path('getdatabycsv', views.getdatabycsv, name='getdatabycsv'),

 path('pay_as_go/<int:expected_price>',views.pay_as_go,name='pay_as_go'),
 path('pay_as_go_success',views.pay_as_go_success,name='pay_as_go_success'),


path('import_data1', views.import_data1,name='import_data1'),
path('import_data2', views.import_data2,name='import_data2'),
path('run_again_query/<int:id>', views.run_again_query,name='run_again_query'),


path('getCountry',views.dropdown_get_country,name="get-country"),
path('getState',views.dropdown_get_state,name="get-state"),

]