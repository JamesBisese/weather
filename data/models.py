from django.db import models

# Contains list of stations that will be used for Weather Data
class Station(models.Model):
    site_code = models.CharField(unique=True, max_length=12, default=None, blank=False, null=False)
    site_name = models.CharField(unique=True, max_length=128, default=None, blank=False, null=False)
    short_name = models.CharField(max_length=128, blank=True, null=True)
    lastretrieval = models.DateTimeField(db_column='LastRetrieval', blank=True, null=True)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.site_code + ' - ' + self.site_name

    class Meta:
        managed = True
        db_table = 'stations'

class WeatherData(models.Model):
    timestamp = models.CharField(db_column='TIMESTAMP', max_length=255, default=None, blank=False, null=False)  # Field name made lowercase.

    station = models.ForeignKey(Station, on_delete=models.CASCADE, default=None, blank=False, null=False)

    # site_code = models.CharField(max_length=12)
    datetime = models.DateTimeField(db_column='DateTime', blank=True, null=True)  # Field name made lowercase.
    date = models.IntegerField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.CharField(db_column='Time', max_length=255, blank=True, null=True)  # Field name made lowercase.
    wind = models.CharField(db_column='Wind', max_length=255, blank=True, null=True)  # Field name made lowercase.
    visibility = models.CharField(db_column='Visibility', max_length=50, blank=True, null=True)  # Field name made lowercase.
    weather = models.CharField(db_column='Weather', max_length=255, blank=True, null=True)  # Field name made lowercase.
    skycondition = models.CharField(db_column='SkyCondition', max_length=255, blank=True, null=True)  # Field name made lowercase.
    airtemp = models.IntegerField(db_column='AirTemp', blank=True, null=True)  # Field name made lowercase.
    dewpoint = models.IntegerField(db_column='Dewpoint', blank=True, null=True)  # Field name made lowercase.
    air6hourmax = models.CharField(db_column='Air6HourMax', max_length=255, blank=True, null=True)  # Field name made lowercase.
    air6hourmin = models.CharField(db_column='Air6HourMin', max_length=255, blank=True, null=True)  # Field name made lowercase.
    relativehumidity = models.CharField(db_column='RelativeHumidity', max_length=255, blank=True, null=True)  # Field name made lowercase.
    windchill = models.CharField(db_column='WindChill', max_length=255, blank=True, null=True)  # Field name made lowercase.
    heatindex = models.CharField(db_column='HeatIndex', max_length=255, blank=True, null=True)  # Field name made lowercase.
    airpressurealtimeter = models.TextField(db_column='AirPressureAltimeter', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    airpressuresealevel = models.CharField(db_column='AirPressureSeaLevel', max_length=255, blank=True, null=True)  # Field name made lowercase.
    precip1h = models.CharField(db_column='Precip1h', max_length=255, blank=True, null=True)  # Field name made lowercase.
    precip3h = models.CharField(db_column='Precip3h', max_length=255, blank=True, null=True)  # Field name made lowercase.
    precip6hr = models.CharField(db_column='Precip6hr', max_length=255, blank=True, null=True)  # Field name made lowercase.
    update_count = models.SmallIntegerField()

    def __str__(self):
        return self.station.site_code + ' - ' + self.station.site_name + ' - ' + self.timestamp

    class Meta:
        managed = True
        db_table = 'weather_data'
        unique_together = (("station", "timestamp"))
