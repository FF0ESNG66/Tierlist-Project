"""
URL configuration for rate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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


urlpatterns = [
    path('create/', include('rating_templates.urls')),
    path('users/',include('users.urls')),
    path('', include('rates_lobby.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')), # Note: This is something related to the login/logout authetication stuff, do NOT delete
    path('accounts/', include('allauth.urls')),  # Note: This is related to Google
]
