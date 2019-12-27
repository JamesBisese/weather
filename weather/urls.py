"""weather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from data.views import StationViewSet, WeatherDataViewSet

router = routers.DefaultRouter()
router.register(r'stations', StationViewSet)
router.register(r'weather', WeatherDataViewSet)

iis_app_alias = ''
if len(settings.IIS_APP_ALIAS) > 0:
    iis_app_alias = settings.IIS_APP_ALIAS + '/'

admin.site.site_url = r'/' + iis_app_alias

urlpatterns = [
    path(iis_app_alias + 'api/', include(router.urls)),

    path(iis_app_alias + 'admin/', admin.site.urls),
    path(iis_app_alias + 'data/', include('data.urls')),
    path(iis_app_alias + 'chart/', include('chart.urls')),

    path(iis_app_alias + '', include('chart.urls')),

]
