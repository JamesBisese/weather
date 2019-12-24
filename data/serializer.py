from rest_framework import serializers

from.models import Station, WeatherData

class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = (
            'site_code',
            'site_name',
            'short_name',
            'lastretrieval',
        )
        # Specifying fields in datatables_always_serialize
        # will also force them to always be serialized.
        # datatables_always_serialize = ('id',)

    # read_only_fields = [f.name for f in Station._meta.get_fields()]

class WeatherDataSerializer(serializers.ModelSerializer):

    site_code = serializers.SerializerMethodField()
    site_name = serializers.SerializerMethodField()
    airpressure = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()

    def get_site_code(self, obj):
        return '%s' % obj.station.site_code
    def get_site_name(self, obj):
        return '%s' % obj.station.site_name
    def get_airpressure(self, obj):
        return float(obj.airpressurealtimeter)
    def get_timestamp(self, obj):
        return int(obj.datetime.timestamp() * 100)
    class Meta:
        model = WeatherData
        # fields = '__all__'
        fields = (
            'site_code',
            'site_name',
            'datetime',
            'timestamp',
            'airtemp',
            'airpressure',
        )
        # exclude = (
        #     'id',
        #     'timestamp',
        #     'air6hourmax',
        #     'air6hourmin',
        #     'airpressuresealevel',
        # )