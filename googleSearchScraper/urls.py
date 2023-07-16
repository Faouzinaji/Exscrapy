"""googleSearchScraper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from googleSearchApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('google_search/', include('googleSearchApp.urls')),
    path('captcha/', include('captcha.urls')),
    path('dashboard/', include('Home.urls')),
    path('', include('authentication.urls')),
    path('get_emails/', include('Get_Emails_from_Domain.urls')),
    # path('social-auth/', include('social_django.urls', namespace='social')),  # <-- here
    path("", include("allauth.urls")),
    path('social/signup/', views.signup_redirect, name='signup_redirect'),

    path('plans/', include('payment_methods.urls')),
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
