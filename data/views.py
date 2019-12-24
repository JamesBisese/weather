from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Station, WeatherData

from .serializer import StationSerializer, WeatherDataSerializer

'''
    provided via /api/stations
'''
class StationViewSet(viewsets.ViewSet):
    queryset = Station.objects.all().order_by('site_code')
    serializer_class = StationSerializer

    def get_queryset(self):
        qs = super(StationViewSet, self).get_queryset()

        site_code = self.request.query_params.get('site_code', None)
        if site_code is not None:
            qs = qs.filter(site_code=site_code)

    def list(self, request):
        # qs = super(StationViewSet, self).get_queryset()
        #
        # site_code = self.request.query_params.get('site_code', None)
        # if site_code is not None:
        #     qs = qs.filter(site_code=site_code)


        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

'''
    provided via /api/weather
'''
class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeatherData.objects.all().order_by('station__site_code')
    serializer_class = WeatherDataSerializer

    def get_queryset(self):
        qs = WeatherData.objects.all().order_by('station__site_code').order_by('timestamp')

        site_code = self.request.query_params.get('site_code', None)
        if site_code is not None:
            station = Station.objects.get(site_code__exact=site_code.upper())
            qs = qs.filter(station=station)
        return qs

    def details(self, request, *args, **kwargs):
        if kwargs and 'site_code' in kwargs:
            site_code = kwargs['site_code']
            station = Station.objects.filter(site_code__exact=site_code)
            self.queryset = WeatherData.objects.filter(station=station).order_by('timestamp')

        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if kwargs and 'site_code' in kwargs:
            site_code = kwargs['site_code']
            station = Station.objects.get(site_code__exact=site_code.upper())
            self.queryset = WeatherData.objects.filter(station=station).order_by('timestamp')

        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)