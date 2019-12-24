from django.contrib import admin

from .models import Station, WeatherData

# admin.site.register(Location)
admin.site.register(Station)
admin.site.register(WeatherData)