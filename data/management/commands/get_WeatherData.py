from django.core.management.base import BaseCommand
import json
import argparse
from datetime import datetime
from django.conf import settings
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404
from django.utils.timezone import make_aware

from urllib.request import urlopen, URLError
from bs4 import BeautifulSoup, UnicodeDammit

from data.models import Station, WeatherData

#
# data is loaded by making an HTTP call and downloading a
# table of data.
#
# Note: I am using this table version because the local weather station
# in Salida KANK is not a full scale station, so the data is not available
# via a more robust API

# (weather) C:\inetpub\wwwdjango\weather> python manage.py get_WeatherData
#
class Command(BaseCommand):
    help = 'Tool to read HTML table of 3-day observation weather data and store in model.' + \
        'reads from web server "' + settings.WEATHER_DATA_URL['URI'] + '"'

    out_file_columns = settings.WEATHER_COLUMN.split(',')

    def add_arguments(self, parser):
        parser.add_argument('-s', '--station',
                            help='station to get data from (ex. ' + ', '.join(Station.objects.all().values_list('site_code', flat=True)) + ')', required=False)
        parser.add_argument("-r", "--runall", action="store_true",
                            help='process (run) all of stations')

    def handle(self, *args, **options):
        site_code = 'KANK'
        if options['station']:
            site_code = options['station']

        station = get_object_or_404(Station, site_code=site_code)

        [LastRetrieval, data_rows] = self.get_data(station)
        if len(data_rows) > 0:
            """
                this is where the data is stored
            """
            [pre_insert_row_count, post_insert_row_count] = self.store_data(station, data_rows, LastRetrieval)

        if post_insert_row_count <= 0:
            print('failed to store data')
        else:
            new_rows = post_insert_row_count - pre_insert_row_count
            print("number of new rows stored %s" % (new_rows))
            station.lastretrieval = make_aware(datetime.now())
            station.save()

    def get_data(self, station):

        url = settings.WEATHER_DATA_URL['URI'] + '/' + station.site_code.upper() + settings.WEATHER_DATA_URL['file_extension']

        print('retrieval url: %s' % (url))

        # Make soup
        try:
            resp = urlopen(url)

            LastRetrieval = datetime.strptime(resp.headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
            # LastModified = datetime.strptime(resp.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S %Z')

            print('web page retrieved: Date: ' + resp.headers['Date'])

            contents = resp.read()
            new_contents = UnicodeDammit.detwingle(contents)
            soup = BeautifulSoup(new_contents, "html.parser")

        except URLError as e:
            print('An error occurred fetching data\n\t%s\n\t%s' % (url, e.reason))
            return {}

        # Get table
        try:
            tables = soup.findAll("table")
            table = tables[3]
        except AttributeError as e:
            print('No tables found, exiting' % (url, e.reason))
            return 1
        except LookupError as e:
            print('there is no index table[3] on the page for ' + url)
            return 1
        except IndexError as e:
            print('there is no index table[3] on the page for ' + url)
            return 1

        # Get rows
        try:
            rows = table.find_all('tr')
        except AttributeError as e:
            print('No table rows found, exiting' % (url, e.reason))
            return 1

        # first two columns are created from the table
        table_columns = self.out_file_columns[3:len(self.out_file_columns)]

        # Get data
        table_data = self.parse_rows(rows)

        # prepare the data read from the web page
        today = datetime.now()
        month = today.month
        year = today.year
        monthedge = 0

        data_rows = {}
        for i in table_data:

            data = dict(zip(table_columns, i))

            day = data['Date']

            # this gets over month/year edges.
            if int(day) <= 2 and monthedge == 0:
                monthedge = 1

            hour, minute = data['Time'].split(':')

            my_month = -1

            # this gets over month/year edges.
            if int(day) > 2 and monthedge == 1:
                my_month = month - 1  # the month is coming from 'localtime' not the webpage
                if my_month == 0:  # january fix
                    my_month = 12
                    year = year - 1
            else:
                my_month = month

            obs_datetime = datetime(year, my_month, int(day), int(hour), int(minute))

            data['site_code'] = station.site_code.upper()
            data['DateTime'] = obs_datetime.strftime('%Y-%m-%d %H:%M:00')
            data['TIMESTAMP'] = 'TS:' + data['DateTime']

            # these fields are stored in the database as numbers, but the web pages use 'NA' for missing data.  that string needs to be replaced with None
            check_field_values = ['AirTemp', 'Dewpoint', 'AirPressureAltimeter']
            for field in check_field_values:
                if data[field] == 'NA':
                    data[field] = None
                elif not data[field]:
                    data[field] = None

            data_rows[data['TIMESTAMP']] = data

        return [LastRetrieval, data_rows]

    def store_data(self, station, data, LastRetrieval):

        if len(data) <= 0:
            return [-1, -1];

        # get the count of existing rows for this station
        count_query = WeatherData.objects.filter(station=station).count()
        pre_insert_row_count = count_query
        print("existing record count==" + str(pre_insert_row_count))

        records = []
        for k, v in sorted(data.items()):

            my_datatime = make_aware(datetime.strptime(v['DateTime'], '%Y-%m-%d %H:%M:00'))

            records.append(WeatherData(
                timestamp = v['TIMESTAMP'],
                station = station,
                datetime = my_datatime,
                date = v['Date'],
                time = v['Time'],
                wind = v['Wind'],
                visibility = v['Visibility'],
                weather = v['Weather'],
                skycondition = v['SkyCondition'],
                airtemp = v['AirTemp'],
                dewpoint = v['Dewpoint'],
                air6hourmax = v['Air6HourMax'],
                air6hourmin = v['Air6HourMin'],
                relativehumidity = v['RelativeHumidity'],
                windchill = v['WindChill'],
                heatindex = v['HeatIndex'],
                airpressurealtimeter = v['AirPressureAltimeter'],
                airpressuresealevel = v['AirPressureSeaLevel'],
                precip1h = v['Precip1h'],
                precip3h = v['Precip3h'],
                precip6hr = v['Precip6hr'],
                update_count = 0,
            ))

        WeatherData.objects.bulk_create(records, ignore_conflicts=True)

        # get the count of existing rows for this station
        count_query = WeatherData.objects.filter(station=station).count()

        post_insert_row_count = count_query

        return [pre_insert_row_count, post_insert_row_count]

    def parse_rows(self, rows):
        """ Get 'table data' from rows """
        results = []
        for row in rows:
            table_data = row.find_all('td')
            if table_data:
                results.append([data.get_text() for data in table_data])

        # remove the 'date' that is the last element in the list
        del results[-1]

        return results


    def decode_html(self, html_string):
        converted = UnicodeDammit(html_string, is_html=True)
        if not converted.unicode:
            raise UnicodeDecodeError(
                "Failed to detect encoding, tried [%s]",
                ', '.join(converted.triedEncodings))

        return converted.unicode