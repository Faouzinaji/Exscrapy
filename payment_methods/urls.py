from django.urls import path
from . import views


urlpatterns = [

    path('payment_success', views.stripe_payment_success,name='thanks_page'),
    path('payment_cancel', views.payment_cancel,name='sorry_page'),
    path('pricing',views.pricing,name='pricing'),
    path('checkout/<int:plan_id>',views.checkout,name='checkout'),
    path('checkout_session/<int:plan_id>',views.checkout_session,name='checkout_session'),
     path('cancel_subscription',views.cancel_subscription,name='cancel_subscription'),

]