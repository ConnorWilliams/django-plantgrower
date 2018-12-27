from django.contrib import admin

from .models import Grow
from .models import InputDevice
from .models import OutputDevice

admin.site.register(Grow)
admin.site.register(InputDevice)
admin.site.register(OutputDevice)
