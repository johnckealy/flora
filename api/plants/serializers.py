from .models import Device, Plant
from rest_framework import serializers



class PlantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plant
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = '__all__'

    def create(self, validated_data):
        device = Device.objects.create(
            nickname = validated_data['nickname'],
            device_id = validated_data['device_id'],
            airtable_plant_id = validated_data['airtable_plant_id'],
            room = validated_data['room'],
            user = validated_data['user'],
            image_url = validated_data['image_url']
        )
        return device


class StatusMessageSerializer(serializers.Serializer):
    color = serializers.CharField()
    message = serializers.CharField()


class HistorySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    date = serializers.CharField()
    message = serializers.CharField()


class AlertsSerializer(serializers.Serializer):
    message = serializers.CharField()
    color = serializers.CharField()
    icon = serializers.CharField()
    date = serializers.CharField()


class StatusSerializer(serializers.Serializer):
    water = StatusMessageSerializer()
    soilmoist = StatusMessageSerializer()
    sun = StatusMessageSerializer()
    temperature = StatusMessageSerializer()
    humidity = StatusMessageSerializer()
    dashboard_message = serializers.CharField()
    alerts = serializers.ListField(AlertsSerializer())



class DashboardInfoSerializer(serializers.Serializer):
    """ Serializer for the dashboard data  """

    user_id = serializers.IntegerField()
    airtable_plant_id = serializers.CharField()
    device_id = serializers.CharField()
    scientific_name = serializers.CharField()
    nickname = serializers.CharField()
    room = serializers.CharField()
    plant_name = serializers.CharField()
    small_thumbnail_url = serializers.CharField()
    current_temp = serializers.DecimalField(max_digits=4, decimal_places=1)
    image_url = serializers.CharField()
    current_humidity = serializers.DecimalField(max_digits=4, decimal_places=1)
    current_soilmoist = serializers.DecimalField(max_digits=4, decimal_places=1)
    current_sun = serializers.IntegerField()
    current_waterlevel_ok = serializers.BooleanField()
    status = StatusSerializer()


class DialogInfoSerializer(serializers.Serializer):
    """ Serializer for the dialog data  """

    user_id = serializers.IntegerField()
    airtable_plant_id = serializers.CharField()
    device_id = serializers.CharField()
    scientific_name = serializers.CharField()
    plant_type = serializers.CharField()
    description = serializers.CharField()
    nickname = serializers.CharField()
    room = serializers.CharField()
    plant_name = serializers.CharField()
    toxicity = serializers.CharField()
    ideal_soil_type = serializers.CharField()
    containers = serializers.CharField()
    water_preference = serializers.CharField()
    image_url = serializers.CharField()
    sun_requirements = serializers.CharField()
    underground_structures = serializers.CharField()
    plant_uses = serializers.CharField()
    current_temp = serializers.DecimalField(max_digits=4, decimal_places=1)
    current_humidity = serializers.DecimalField(max_digits=4, decimal_places=1)
    current_soilmoist = serializers.DecimalField(max_digits=4, decimal_places=1)
    current_sun = serializers.IntegerField()
    current_waterlevel_ok = serializers.BooleanField()
    temperature_history = serializers.StringRelatedField(many=True)
    humidity_history = serializers.StringRelatedField(many=True)
    soilmoist_history = serializers.StringRelatedField(many=True)
    sun_history = serializers.StringRelatedField(many=True)
    small_thumbnail_url = serializers.CharField()
    large_thumbnail_url = serializers.CharField()
    datetime_history = serializers.StringRelatedField(many=True)
    dialog_status = StatusSerializer()

