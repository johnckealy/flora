from django.urls import path
from .views import (DeviceDetail, DashboardInfo, DialogInfo,
                    HistoryIndex, PlantIndex, PlantDetail,
                    ManualIntegration, ImageUploadView )

urlpatterns = [
    path('plants_index/', PlantIndex.as_view(), name='plants'),
    path('plant_detail/<str:airtable_id>', PlantDetail.as_view(), name='plant_detail'),
    path('add_device/', DeviceDetail.as_view(), name='device_create'),
    path('delete_device/<str:device_id>/', DeviceDetail.as_view(), name='device_destroy'),
    path('devices/<int:pk>/', DeviceDetail.as_view(), name='device_detail'),
    path('history/', HistoryIndex.as_view(), name='history_index'),
    path('manual_integration/', ManualIntegration.as_view(), name='history_index'),
    path('dashboard_data/', DashboardInfo.as_view(), name='device_detail'),
    path('dialog_data/<str:device_id>/', DialogInfo.as_view(), name='dialogue_detail'),

    path('upload/', ImageUploadView.as_view())

]