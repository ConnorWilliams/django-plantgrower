import os
import sys
import channels.asgi

sys.path.append('/home/pi/plant_grower')
sys.path.append(
    '/home/pi/.virtualenvs/plantgrower/lib/python3.5/site-packages/'
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_grower.settings")

channel_layer = channels.asgi.get_channel_layer()
