import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from data.models import Station, WeatherData

class Index(generic.TemplateView):

    stations = Station.objects.all()

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context_data = super(Index, self).get_context_data(**kwargs)

        context_data['stations'] = self.stations
        context_data['stationA'] = self.stations[0]
        context_data['stationB'] = self.stations[1]

        return context_data