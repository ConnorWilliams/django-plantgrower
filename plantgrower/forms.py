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
            'turned_on'
        ]