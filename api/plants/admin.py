from django.contrib import admin
from .models import Device, Plant, ReadingHistory, PlantToleranceLimits, AlertsCopy, EventHistory

# Register your models here.
admin.site.register(Device)
admin.site.register(Plant)
admin.site.register(PlantToleranceLimits)
admin.site.register(ReadingHistory)
admin.site.register(AlertsCopy)
admin.site.register(EventHistory)