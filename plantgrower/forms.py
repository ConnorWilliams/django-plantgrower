from django.forms import ModelForm
from .models import Grow, InputDevice, OutputDevice


# Create the form class.
class GrowForm(ModelForm):
    class Meta:
        model = Grow
        fields = [
            'strain',
            'veg_light_duration',
            'flower_light_duration',
            'temperature',
            'humidity'
        ]


class InputDeviceForm(ModelForm):
    class Meta:
        model = InputDevice
        exclude = [
            'grow'
        ]

class OutputDeviceForm(ModelForm):
    class Meta:
        model = OutputDevice
        exclude = [
            'grow',
            'system_status',
            'user_status'
        ]
