from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from django.contrib.auth.models import User
from .models import Device, Plant, EventHistory
from .serializers import (DashboardInfoSerializer, DeviceSerializer,
                          DialogInfoSerializer, PlantSerializer, HistorySerializer)
from .status_service import StatusService
from .tasks import manual_integration
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from .image_service import image_service
from django.utils.crypto import get_random_string



class PlantIndex(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlantSerializer
    queryset = Plant.objects.all()


class PlantDetail(APIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'airtable_id'

    def get(self, request, airtable_id):
        plant = Plant.objects.get(airtable_id=airtable_id)
        plant_data = PlantSerializer(plant).data
        return Response(plant_data)


class DeviceDetail(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceSerializer
    lookup_field = 'device_id'

    def get(self, request, pk):
        device =  Device.objects.get(pk=pk)
        serializer = DeviceSerializer(device)
        return Response(serializer.data)

    def post(self, request):
        if Device.objects.filter(device_id=request.data['device_id']).count() > 0:
            return Response({
                "error": "Device registration failed. That device ID has already been registered."
            })
        data = request.data
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        device = serializer.save()
        return Response({
            "device": DeviceSerializer(device, context=self.get_serializer_context()).data,
            "message": "Device Created Successfully. "
        })

    def delete(self, request, device_id):
        device = Device.objects.get(device_id=device_id)
        device.delete()
        return Response({
            "message": f"Device {device_id} deleted successfully."
        })


class ManualIntegration(APIView):

    permission_classes = (IsAuthenticated,)
    def get(self, request):
        manual_integration.delay()
        return Response({
            "message": f"Integration script was triggered."
        })


class DashboardInfo(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        devices = user.device_set
        dashboard_data = []
        for device in devices.all():
            try:
                plant = Plant.objects.get(airtable_id=device.airtable_plant_id)
            except Plant.DoesNotExist:
                raise ValueError('The entry was not found in the plant database. Have you run the sync script?')

            status = StatusService(device, plant).plant_status()

            dashboard_data.append({
                "user_id": device.user_id,
                "device_id": device.device_id,
                'room': device.room,
                'nickname': device.nickname,
                'current_temp': device.current_temp,
                'current_humidity': device.current_humidity,
                'image_url': device.image_url,
                'current_soilmoist': device.current_soilmoist,
                'current_sun': device.current_sun,
                'current_waterlevel_ok': device.current_waterlevel_ok,
                "airtable_plant_id": device.airtable_plant_id,
                'scientific_name': plant.scientific_name,
                'plant_name': plant.plant_name,
                'small_thumbnail_url': plant.small_thumbnail_url,
                'status': status
            })

        users_devices = DashboardInfoSerializer(dashboard_data, many=True).data
        return Response(users_devices)


class HistoryIndex(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        limit = request.query_params.get('limit')
        if limit:
            limit = int(limit)
        else:
            limit=10
        histories = EventHistory.objects.filter(user=user).order_by('-updated_at')[:limit]
        history_index = [ HistorySerializer(history).data for history in histories ]

        return Response(history_index)


class DialogInfo(APIView):

    permission_classes = (IsAuthenticated,)
    lookup_field = 'device_id'

    def get(self, request, device_id):
        user = request.user
        device = Device.objects.get(device_id=int(device_id))
        plant = Plant.objects.get(airtable_id=device.airtable_plant_id)

        readinghistory = device.readinghistory_set.all()
        temperature_history = readinghistory.values_list('temperatureF', flat=True)
        humidity_history = readinghistory.values_list('humidity', flat=True)
        soilmoist_history = readinghistory.values_list('soilmoist', flat=True)
        sun_history = readinghistory.values_list('sun', flat=True)
        datetime_history = readinghistory.values_list('valid_datetime', flat=True)
        dialog_status = StatusService(device, plant).plant_status()

        dialog = {
            "user_id": device.user_id,
            "device_id": device.device_id,
            'room': device.room,
            'nickname': device.nickname,
            "airtable_plant_id": device.airtable_plant_id,
            'scientific_name': plant.scientific_name,
            'containers': plant.containers,
            'toxicity': plant.toxicity,
            'ideal_soil_type': plant.ideal_soil_type,
            'water_preference': plant.water_preference,
            'sun_requirements': plant.sun_requirements,
            'underground_structures': plant.underground_structures,
            'plant_uses': plant.plant_uses,
            'plant_name': plant.plant_name,
            'image_url': device.image_url,
            'description': plant.description,
            'plant_type': plant.plant_type,
            'datetime_history': datetime_history,
            'current_temp': device.current_temp,
            'current_humidity': device.current_humidity,
            'current_soilmoist': device.current_soilmoist,
            'current_sun': device.current_sun,
            'current_waterlevel_ok': device.current_waterlevel_ok,
            'temperature_history': temperature_history,
            'humidity_history': humidity_history,
            'soilmoist_history': soilmoist_history,
            'sun_history': sun_history,
            'small_thumbnail_url': plant.small_thumbnail_url,
            'large_thumbnail_url': plant.large_thumbnail_url,
            'dialog_status': dialog_status
        }

        dialog_data = DialogInfoSerializer(dialog).data
        return Response(dialog_data)




class ImageUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request):
        """Upload a user image to the DigitOcean Spaces
        bucket."""
        try:
            if request.method == 'POST':
                for filename in request.FILES:
                    key = filename
                image = request.FILES[key]
                name, ext = os.path.splitext(image.name)
                filename = f"{name}-{get_random_string(9)}{ext}"
                bucketname = os.path.splitext(request.user.username)[0].replace('@', 'at')
                image_url = image_service(image, bucket=bucketname, filename=filename)
                return Response(image_url, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {'error': 'There was a problem uploading your image. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
