from plants.models import AlertsCopy
from datetime import datetime
class StatusService:

    GOOD_DASHBOARD_MESSAGE = f"Everything is looking good!"
    BAD_DASHBOARD_MESSAGE = f"Your plant isn't situated in its ideal conditions. Click SEE MORE for details."


    def __init__(self, device, plant):
        self.device = device
        self.plant = plant
        self.alerts = []
        self.dashboard_message = self.GOOD_DASHBOARD_MESSAGE


    def plant_status(self):
        return {
            'water': self.water_status(),
            'sun': self.sun_status(),
            'temperature': self.temperature_status(),
            'soilmoist': self.soilmoist_status(),
            'humidity': self.humidity_status(),
            'alerts': self.alerts,
            'dashboard_message': self.dashboard_message
        }


    def if_else_maze(self, field_name, current_field, alert_lower, alert_upper, warning_lower, warning_upper, alerts_copy, plant_name, room):
        if current_field is not None:
            if alert_lower:
                if current_field < alert_lower:
                    self.alerts.append({
                        "message": f"{self.device.nickname}: {field_name} alert.",
                        "color": "negative",
                        "icon": "mdi-alert-outline",
                        "date": datetime.now().strftime("%m/%d/%Y")
                    })
                    self.dashboard_message = self.BAD_DASHBOARD_MESSAGE
                    return {
                        'color': 'negative',
                        'message': alerts_copy.alert_lower_copy
                    }
            if alert_upper:
                if current_field > alert_upper:
                    self.alerts.append({
                        "message": f"{self.device.nickname}: {field_name} alert.",
                        "color": "negative",
                        "icon": "mdi-alert-outline",
                        "date": datetime.now().strftime("%m/%d/%Y")
                    })
                    self.dashboard_message = self.BAD_DASHBOARD_MESSAGE
                    return {
                        'color': 'negative',
                        'message': alerts_copy.alert_upper_copy
                    }
            if warning_upper:
                if current_field > warning_upper:
                    self.alerts.append({
                        "message": f"{self.device.nickname}: {field_name} issue.",
                        "color": "warning",
                        "icon": "mdi-bell-alert-outline",
                        "date": datetime.now().strftime("%m/%d/%Y")
                    })
                    self.dashboard_message = self.BAD_DASHBOARD_MESSAGE
                    return {
                        'color': 'warning',
                        'message': alerts_copy.warning_upper_copy
                    }
            if warning_lower:
                if current_field < warning_lower:
                    self.alerts.append({
                        "message": f"{self.device.nickname}: {field_name} issue.",
                        "color": "warning",
                        "icon": "mdi-bell-alert-outline",
                        "date": datetime.now().strftime("%m/%d/%Y")
                    })
                    self.dashboard_message = self.BAD_DASHBOARD_MESSAGE
                    return {
                        'color': 'warning',
                        'message': alerts_copy.warning_upper_copy
                    }
            return {
                'color': 'accent',
                'message': f"The {field_name} for the {plant_name} in your {room} is just right!"
            }
        else:
            self.dashboard_message = self.BAD_DASHBOARD_MESSAGE
            self.alerts.append({
                'message': f"There is no {field_name} information for {self.device.nickname}.",
                "color": "warning",
                "icon": "mdi-bell-alert-outline",
                "date": datetime.now().strftime("%m/%d/%Y")
            })
            return {
                'color': 'warning',
                'message': f"There is no {field_name} information for the {plant_name} in your {room}."
            }


    def temperature_status(self):
        alerts_copy = AlertsCopy.objects.get(field_name='Temperature')

        return self.if_else_maze(
            field_name='temperature',
            current_field=self.device.current_temp,
            alert_lower=self.plant.temp_limits.alert_lower,
            alert_upper=self.plant.temp_limits.alert_upper,
            warning_lower=self.plant.temp_limits.warning_lower,
            warning_upper=self.plant.temp_limits.warning_upper,
            alerts_copy=alerts_copy,
            plant_name=self.plant.plant_name,
            room=self.device.room
        )


    def humidity_status(self):
        alerts_copy = AlertsCopy.objects.get(field_name='Humidity')

        return self.if_else_maze(
            field_name='humidity',
            current_field=self.device.current_humidity,
            alert_lower=self.plant.humidity_limits.alert_lower,
            alert_upper=self.plant.humidity_limits.alert_upper,
            warning_lower=self.plant.humidity_limits.warning_lower,
            warning_upper=self.plant.humidity_limits.warning_upper,
            alerts_copy=alerts_copy,
            plant_name=self.plant.plant_name,
            room=self.device.room
        )

    def water_status(self):
        alerts_copy = AlertsCopy.objects.get(field_name='Reservoir ')
        if self.device.current_waterlevel_ok:
            return {
                'color': 'accent',
                'message':  f"The water reservoir for the {self.plant.plant_name} in your {self.device.room} is fine."
            }
        elif self.device.current_waterlevel_ok==False:
            self.dashboard_message = self.BAD_DASHBOARD_MESSAGE
            self.alerts.append({
                "message": f"{self.device.nickname}: {alerts_copy.alert_lower_copy}",
                "color": "negative",
                "icon": "mdi-alert-outline",
                "date": datetime.now().strftime("%m/%d/%Y")
            })
            return {
                'color': 'negative',
                'message': alerts_copy.alert_lower_copy
            }

        else:
            self.dashboard_message = self.BAD_DASHBOARD_MESSAGE
            return {
                'color': 'warning',
                'message': f"There is no water information for the {self.plant.plant_name}  in your {self.device.room}."
            }


    def soilmoist_status(self):
        alerts_copy = AlertsCopy.objects.get(field_name='Soil Moisture')

        return self.if_else_maze(
            field_name='soil moisture',
            current_field=self.device.current_soilmoist,
            alert_lower=self.plant.soilmoist_limits.alert_lower,
            alert_upper=self.plant.soilmoist_limits.alert_upper,
            warning_lower=self.plant.soilmoist_limits.warning_lower,
            warning_upper=self.plant.soilmoist_limits.warning_upper,
            alerts_copy=alerts_copy,
            plant_name=self.plant.plant_name,
            room=self.device.room
        )


    def sun_status(self):
        alerts_copy = AlertsCopy.objects.get(field_name='Light')

        return self.if_else_maze(
            field_name='sunlight',
            current_field=self.device.current_sun,
            alert_lower=self.plant.sun_limits.alert_lower,
            alert_upper=self.plant.sun_limits.alert_upper,
            warning_lower=self.plant.sun_limits.warning_lower,
            warning_upper=self.plant.sun_limits.warning_upper,
            alerts_copy=alerts_copy,
            plant_name=self.plant.plant_name,
            room=self.device.room
        )


