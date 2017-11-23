from django.forms import ModelForm
from .models import Grow


# Create the form class.
class GrowForm(ModelForm):
    class Meta:
        model = Grow
        fields = '__all__'
        # fields = ['strain', 'current_stage']
