import requests
from plants.models import Plant, PlantToleranceLimits, AlertsCopy
from .utils import Lcolors, LOG, CLOG

API_KEY = 'keydGMEOXdcE5ej1d'

AIRTABLE_HP_URL = f'https://api.airtable.com/v0/appnWM0Jpni53knmd/Houseplant%20Master%20List?api_key={API_KEY}'

# soil moisture 12
# all other 24hr

def alerts():

    AIRTABLE_ALERTS_URL = f'https://api.airtable.com/v0/appnWM0Jpni53knmd/Alert%20Copy?api_key={API_KEY}'

    response = requests.get(AIRTABLE_ALERTS_URL)
    alerts = response.json()['records']

    for alert in alerts:
        try:
            AlertsCopy.objects.create(
                field_name=alert['fields']['Name'],
                alert_lower_copy=alert['fields']['Red Alert Too low'],
                alert_upper_copy=alert['fields']['Red Alert Too high'],
                warning_lower_copy=alert['fields']['Yellow Alert Low'],
                warning_upper_copy=alert['fields']['Yellow Alert High'],
            )
        except KeyError:
            if 'Name' in alert['fields'].keys():
                if alert['fields']['Name'] == 'Reservoir ':
                    AlertsCopy.objects.create(
                        field_name='Reservoir ',
                        alert_lower_copy=alert['fields']['Red Alert Too low']
                    )
            else:
                LOG.warning(f"{Lcolors.WARNING} ### WARNING: {Lcolors.ENDC} An alert copy entry was missing keys.")



def sync():
    """ Syncronization script for getting airtable plant data into the
    local database. Deletes everything in the local Plant database;
    the idea is to keep airtable as the unique source of truth
    and stay up to date with that."""


    response = requests.get(AIRTABLE_HP_URL)
    plants = response.json()['records']

    for plant in plants:
        fields = plant['fields']
        airtable_id = plant['id']
        plant_name = fields['Plant Name']  if 'Plant Name' in fields.keys() else None
        description = fields['Plant Description']  if 'Plant Description' in fields.keys() else None
        plant_type = fields['Plant Type']  if 'Plant Type' in fields.keys() else None
        scientific_name = fields['Scientific Name'] if 'Scientific Name' in fields.keys() else None
        containers = fields['Containers'] if 'Containers' in fields.keys() else None
        toxicity = fields['Toxicity'][0] if 'Toxicity' in fields.keys() else None
        ideal_soil_type = fields['Soil Type'] if 'Soil Type' in fields.keys() else None
        water_preference = fields['Water Preferences'] if 'Water Preferences' in fields.keys() else None
        sun_requirements = fields['Sun Requirements'] if 'Sun Requirements' in fields.keys() else None
        plant_uses = fields['Uses'] if 'Uses' in fields.keys() else None
        underground_structures = fields['Underground structures'] if 'Underground structures' in fields.keys() else None

        temp_limits = PlantToleranceLimits.objects.create(
            warning_lower = fields['Temperature Low Yellow Alert'] if 'Temperature Low Yellow Alert' in fields.keys() else None,
            warning_upper = fields['Temperature High Yellow Alert'] if 'Temperature High Yellow Alert' in fields.keys() else None,
            alert_lower = fields['Temperature Low Red Alert'] if 'Temperature Low Red Alert' in fields.keys() else None,
            alert_upper = fields['Temperature High Red Alert'] if 'Temperature High Red Alert' in fields.keys() else None
        )
        sun_limits = PlantToleranceLimits.objects.create(
            warning_lower = fields['Light Low Yellow Alert'] if 'Light Low Yellow Alert' in fields.keys() else None,
            warning_upper = fields['Light High Yellow Alert'] if 'Light High Yellow Alert' in fields.keys() else None,
            alert_lower = fields['Light Low Red Alert'] if 'Light Low Red Alert' in fields.keys() else None,
            alert_upper = fields['Light High Red Alert'] if 'Light High Red Alert' in fields.keys() else None
        )
        soilmoist_limits = PlantToleranceLimits.objects.create(
            warning_lower = fields['Soil Moisture Low Yellow Alert'] if 'Soil Moisture Low Yellow Alert' in fields.keys() else None,
            warning_upper = fields['Soil Moisture High Yellow Alert'] if 'Soil Moisture High Yellow Alert' in fields.keys() else None,
            alert_lower = fields['Soil Moisture Low Red Alert'] if 'Soil Moisture Low Red Alert' in fields.keys() else None,
            alert_upper = fields['Soil Moisture High Red Alert'] if 'Soil Moisture High Red Alert' in fields.keys() else None
        )
        humidity_limits = PlantToleranceLimits.objects.create(
            warning_lower = fields['Humidity Low Yellow Alert'] if 'Humidity Low Yellow Alert' in fields.keys() else None,
            warning_upper = fields['Humidity High Yellow Alert'] if 'Humidity High Yellow Alert' in fields.keys() else None,
            alert_lower = fields['Humidity Low Red Alert'] if 'Humidity Low Red Alert' in fields.keys() else None,
            alert_upper = fields['Humidity High Red Alert'] if 'Humidity High Red Alert' in fields.keys() else None
        )

        if not temp_limits.alert_lower:
            LOG.warning(f"{Lcolors.WARNING} ### WARNING: {Lcolors.ENDC} Temperature Limits were not retrieved for {plant_name}. Please check the sync script.")

        if 'Photos' in fields.keys():
            small_thumbnail_url = fields['Photos'][0]['thumbnails']['small']['url']
            large_thumbnail_url = fields['Photos'][0]['thumbnails']['large']['url']
        else:
            small_thumbnail_url = None
            large_thumbnail_url = None

        Plant.objects.create(
            airtable_id=airtable_id,
            scientific_name=scientific_name,
            plant_name=plant_name,
            description=description,
            plant_type=plant_type,
            small_thumbnail_url=small_thumbnail_url,
            large_thumbnail_url=large_thumbnail_url,
            temp_limits=temp_limits,
            sun_limits=sun_limits,
            soilmoist_limits=soilmoist_limits,
            humidity_limits=humidity_limits,
            ideal_soil_type=ideal_soil_type,
            toxicity=toxicity,
            containers=containers,
            water_preference=water_preference,
            sun_requirements=sun_requirements,
            plant_uses=plant_uses,
            underground_structures=underground_structures
        )




def run():
    LOG.warning(f"{Lcolors.INFO} ### INFO: {Lcolors.ENDC} Deleting all plant records and starting fresh...")
    Plant.objects.all().delete()
    PlantToleranceLimits.objects.all().delete()
    AlertsCopy.objects.all().delete()

    LOG.warning(f"{Lcolors.INFO} ### INFO: {Lcolors.ENDC} Syncing Plant database with Airtable...")
    alerts()
    sync()

    LOG.warning(f"\n{Lcolors.SUCCESS} --- Airtable synced sucessfully. ---{Lcolors.ENDC}\n")