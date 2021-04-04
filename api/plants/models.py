from django.db import models
from django.contrib.auth.models import User


class PlantToleranceLimits(models.Model):
    """ Limits for the tolerance of each plant to various device fields. """
    warning_lower = models.IntegerField(null=True)
    warning_upper = models.IntegerField(null=True)
    alert_lower = models.IntegerField(null=True)
    alert_upper = models.IntegerField(null=True)


class Plant(models.Model):
    """Populated by airtable via the sync script. Bear in mind
    that a change to the airtable schema can break this."""

    airtable_id = models.CharField(max_length=70, null=True)
    scientific_name = models.CharField(max_length=170, null=True)
    plant_name = models.CharField(max_length=70, null=True)
    plant_type = models.CharField(max_length=70, null=True)
    description = models.CharField(max_length=300, null=True)
    sun_limits = models.ForeignKey(PlantToleranceLimits, on_delete=models.CASCADE, related_name='sun_limits', null=True)
    temp_limits = models.ForeignKey(PlantToleranceLimits, on_delete=models.CASCADE, related_name='temp_limits', null=True)
    soilmoist_limits = models.ForeignKey(PlantToleranceLimits, on_delete=models.CASCADE, related_name='soilmoist_limits', null=True)
    humidity_limits = models.ForeignKey(PlantToleranceLimits, on_delete=models.CASCADE, related_name='humidity_limits', null=True)
    ideal_soil_type = models.CharField(max_length=170, null=True)
    toxicity = models.CharField(max_length=170, null=True)
    containers = models.CharField(max_length=170, null=True)
    water_preference = models.CharField(max_length=170, null=True)
    sun_requirements = models.CharField(max_length=170, null=True)
    underground_structures = models.CharField(max_length=170, null=True)
    plant_uses = models.CharField(max_length=170, null=True)
    small_thumbnail_url = models.CharField(max_length=170, null=True)
    large_thumbnail_url = models.CharField(max_length=170, null=True)

    def __str__(self):
        return self.plant_name


class Device(models.Model):
    """Devices are the center-piece of the app. Each registered
    device creates an entry in the dashboard."""
    nickname = models.CharField(max_length=70)
    room = models.CharField(max_length=70)
    device_id = models.CharField(max_length=70, unique=True)
    airtable_plant_id = models.CharField(max_length=70)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_temp = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    current_humidity = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    current_soilmoist = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    current_sun = models.IntegerField(null=True)
    current_waterlevel_ok = models.BooleanField(null=True)
    image_url = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.nickname


class ReadingHistory(models.Model):
    """The reading history is used to populate the graphs in the dialog."""
    temperatureF = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    humidity = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    soilmoist = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    sun = models.IntegerField(null=True)
    valid_datetime = models.DateTimeField()
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    entry_id = models.CharField(max_length=70, null=True)

    def __str__(self):
        return f'Reading History until {self.valid_datetime}'


class EventHistory(models.Model):

    class Meta:
         ordering = ['updated_at']

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=400, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def date(self):
        return self.created_at.strftime('%m/%d/%Y  %H:%M:%S')


class AlertsCopy(models.Model):
    field_name = models.CharField(max_length=400, null=True)
    warning_lower_copy = models.CharField(max_length=400, null=True)
    warning_upper_copy = models.CharField(max_length=400, null=True)
    alert_lower_copy = models.CharField(max_length=400, null=True)
    alert_upper_copy = models.CharField(max_length=400, null=True)

    def __str__(self):
        return f'AlertsCopy {self.field_name}'