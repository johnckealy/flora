import requests
from dateutil import parser, tz
from plants.models import Device, ReadingHistory, EventHistory
from .utils import Lcolors, LOG
from rest_framework import status
from datetime import datetime, timedelta




class ThingSpeakIntegration:

    def __init__(self, device_id, reading_hist_days, averaging_window):
        self.device_id = device_id
        self.reading_hist_days = reading_hist_days
        self.averaging_window = averaging_window

    def verify_channel_info(self, channel_info):
        """Check that the schema returned from ThingSpeak is as expected.
        if the schema changes, then the app will break, since the fields
        are bound to keys like 'field3' etc. """
        CHANNEL_KEYS = {
            "field1": "Humidity",
            "field2": "V.Bat",
            "field3": "Temperature F",
            "field4": "Pump 1",
            "field5": "Lux",
            "field6": "Soil Moisture",
            "field7": "Pump 2",
            "field8": "Water Level"
        }
        for key in CHANNEL_KEYS.keys():
            if channel_info[key] != CHANNEL_KEYS[key]:
                LOG.warning(f"{Lcolors.WARNING} ### WARNING: {Lcolors.ENDC} The Thingspeak keys appear to have changed. Please amend the schema in the thingspeak_integration.py script.")
                return False
        return True


    def set_last_watering_time(self, device, feed):
        if feed['field4']:
            if int(float(feed['field4'])) != 0:
                dt = parser.parse(feed['created_at'])
                if EventHistory.objects.filter(updated_at=dt).count() == 0:
                    history_entry = EventHistory.objects.create(user=device.user, device=device, message=f"{device.knickname} was watered.")
                    history_entry.updated_at = dt
                    history_entry.save()

    def get_instantaneous_fields(self):
        THINGSPEAK_URL = f'https://api.thingspeak.com/channels/{self.device_id}/feeds.json?results=1'
        response = requests.get(THINGSPEAK_URL)
        res = response.json()
        feed = res['feeds'][0]
        channel = res['channel']

        if feed['entry_id'] != channel['last_entry_id']:
            LOG.warning(f"{Lcolors.WARNING} ### WARNING WHILE RETRIEVING THE CURRENT WATER LEVEL: {Lcolors.ENDC} The feed entry id did not match the most recent channel. Please check the integration script.")

        return {
            'water_level_ok': feed['field8'] == '1',
            'current_datetime': parser.parse(feed['created_at']).replace(tzinfo=tz.tzlocal()),
            'current_temp': float(feed['field3']),
            'current_humidity': float(feed['field1']),
            'current_soilmoist': float(feed['field6']),
            'current_sun': float(feed['field5']),
        }


    def get_json(self, response):
        """ Quick helper function to simplify the tests """
        return response.json()

    def process_device(self):
        """ Polling script to read device data from the thingspeak api,
        then populate the django app's database with it"""

        THINGSPEAK_URL = f'https://api.thingspeak.com/channels/{self.device_id}/feeds.json?average={self.averaging_window}'


        LOG.warning(f"{Lcolors.INFO} ### INFO: {Lcolors.ENDC} Hitting the end point: {THINGSPEAK_URL}")

        response = requests.get(THINGSPEAK_URL)
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            LOG.warning(f"{Lcolors.WARNING} ### WARNING: {Lcolors.ENDC} Device with Id {self.device_id} was requested but not found in the database.")
            return False
        if response.status_code == status.HTTP_404_NOT_FOUND:
            LOG.warning(f"{Lcolors.WARNING} ### WARNING: {Lcolors.ENDC} 404 (not found) while attempting to fetch device {self.device_id}.")
            return False

        channel_info = self.get_json(response)['channel']
        feeds = self.get_json(response)['feeds']

        channel_info = self.verify_channel_info(channel_info)

        # Not sure if I want this, its a little too general. Should really error out.
        if not channel_info:
            return False

        instantaneous_fields = self.get_instantaneous_fields()

        try:
            device = Device.objects.get(device_id=self.device_id)
        except Device.DoesNotExist:
            LOG.warning(f"{Lcolors.WARNING} ### WARNING: {Lcolors.ENDC} Device with ID {self.device_id} is not in the database.")
        else:
            datetimes = [ parser.parse(feed['created_at']) for feed in feeds ]
            latest_index = datetimes.index(max(datetimes))
            for index, feed in enumerate(feeds):
                if index == latest_index:
                    device.current_temp = float(feed['field3'])
                    device.current_humidity = float(feed['field1'])
                    device.current_soilmoist = float(feed['field6'])
                    device.current_sun = int(float(feed['field5']))
                    device.current_waterlevel_ok = instantaneous_fields['water_level_ok']
                    device.save()

                self.set_last_watering_time(device, feed)

                if (datetime.now().replace(tzinfo=tz.tzlocal()) - parser.parse(feed['created_at'])).days < self.reading_hist_days:
                    if feed['field1']:
                        ReadingHistory.objects.create(
                            temperatureF=feed['field3'],
                            humidity=feed['field1'],
                            soilmoist=feed['field6'],
                            sun=int(float(feed['field5'])),
                            valid_datetime=datetimes[index],
                            device_id=device,
                        )
        return True



def run():
    LOG.info(f"Running ThingSpeak Integration...")
    devices = Device.objects.all()
    ReadingHistory.objects.all().delete()
    for device in devices:
        EventHistory.objects.create(user=device.user, device=device, message=f"FlorA updated its data for '{device.knickname}'")
        thingspeak = ThingSpeakIntegration(device_id=device.device_id, reading_hist_days=15, averaging_window=1440)
        succeeded = thingspeak.process_device()
        if succeeded:
            LOG.info(f"{Lcolors.INFO} ### INFO: {Lcolors.ENDC} ThingSpeak Integration for device {device.device_id} ran successfully.")
    LOG.info(f"\n{Lcolors.SUCCESS} --- ThingSpeak integration complete. ---{Lcolors.ENDC}\n")
