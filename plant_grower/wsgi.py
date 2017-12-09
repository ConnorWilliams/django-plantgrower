"""
WSGI config for plant_grower project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/pi/plant_grower')
sys.path.append(
    '/home/pi/.virtualenvs/plantgrower/lib/python3.5/site-packages/'
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_grower.settings")

application = get_wsgi_application()
