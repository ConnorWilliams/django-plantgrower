# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from plantgrower.models import Grow, OutputDevice
from django.utils import timezone
from plantgrower.serializers import GrowSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
logger = logging.getLogger(__name__)


@shared_task
def send_grow_information(path):
    """
    Sends grow information over WebSocket to front-end for realtime updates
    """
    grow_id = path.rsplit('-', 1)[-1]
    grow = Grow.objects.get(pk=int(grow_id))
    serializer = GrowSerializer(grow)
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            path, {"type": "send.grow", "text": serializer.data}
        )
    except Exception as e:
        logger.error('Could not send grow info - {}'.format(e))


@shared_task
def monitor_devices():
    """
    Runs on a schedule
    Gets all devices from the DB and queues up monitor_<dvc> for each
    """
    output_devices = OutputDevice.objects.all()
    for output_device in output_devices:
        if output_device.category == 'light':
            monitor_light.delay(output_device.light)


@shared_task
def monitor_light(light):
    """
    Sets grow_state by looking at time and veg_light_duration
    Looks at light.user_state and light.grow_state
    Then sends instructions to the IoT device queue to turn the light on or off
    """
    grow = Grow.objects.get(pk=light.grow_id)
    if timezone.localtime(timezone.now()) > light.next_switch_time:
        # Switch light in DB
        light.last_switch_time = light.next_switch_time
        light.next_switch_time += \
            grow.dark_duration if light.grow_state else grow.light_duration
        light.grow_state = not light.grow_state
        light.save()

    send_device_instruction(light)


@shared_task
def send_device_instruction(output_device):
    # Send instruction to IoT device queue to turn device on or off
    if output_device.user_state is not None:
        logger.info(f"Sending instruction to turn device {output_device.user_status} from user_status")
    else:
        logger.info(f"Sending instruction to turn light {output_device.system_status}")
