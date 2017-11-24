from django.forms import ModelForm
from .models import Grow


# Create the form class.
class GrowForm(ModelForm):
    class Meta:
        model = Grow
        fields = [
            'strain',
            'veg_light_duration',
            'veg_dark_duration',
            'flower_light_duration',
            'flower_dark_duration'
        ]
