from django.urls import path
from . import views


urlpatterns=[
    path('', views.dashboard, name='dashboard'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('notification/', views.Notifications.as_view(), name='notification'),
    path(
        'update/profile/<int:pk>/', views.UpdateProfileView.as_view(),
        name='update_profile'
    ),
    path('Settings', views.Setting, name='Settings'),
    path('setting_security', views.setting_security, name='setting_security'),
    path('contact_us', views.contact_us, name='contact_us'),
]
