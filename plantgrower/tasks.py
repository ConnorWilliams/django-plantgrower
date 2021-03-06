# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from plantgrower.models import Grow, OutputDevice, Light
from plantgrower.publisher import AMQPPublisher
from django.utils import timezone
from plantgrower.serializers import GrowSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import paho.mqtt.publish as publish
import logging
logger = logging.getLogger(__name__)


@shared_task(ignore_result=True)
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
        logger.error('Could not send grow info.')
        raise e


@shared_task(ignore_result=True)
def monitor_devices():
    """
    Runs on a schedule
    Gets all devices from the DB and queues up monitor_<dvc> for each
    """
    output_devices = OutputDevice.objects.all()
    for output_device in output_devices:
        if output_device.category == 'light':
            monitor_light.delay(output_device.pk)


@shared_task(ignore_result=True)
def monitor_light(light_id):
    """
    Sets grow_state by looking at time and veg_light_duration
    Looks at light.user_state and light.grow_state
    Then sends instructions to the IoT device queue to turn the light on or off
    """
    light = Light.objects.get(pk=light_id)
    if light.grow.current_stage in ['2', '3'] and \
            timezone.localtime(timezone.now()) > light.next_switch_time:
        # Switch light in DB
        light.last_switch_time = light.next_switch_time
        light.next_switch_time += \
            light.grow.dark_duration if light.system_status \
            else light.grow.light_duration
        light.system_status = not light.system_status
        light.save()

    send_device_instruction(light.output_device)


@shared_task(ignore_result=True)
def switch_device(output_device_id, status=None):
    output_device = OutputDevice.objects.get(pk=output_device_id)
    output_device.user_status = status
    output_device.save()


def send_device_instruction(output_device):
    """
    Send instruction to IoT device queue to turn device on or off
    """
    status = output_device.system_status
    if output_device.user_status is not None:
        status = output_device.user_status

    publish.single(
        f"grow/{output_device.grow_id}/output",
        str((output_device.pin, status)),
        hostname="mosquitto"
    )


def send_amqp_message(grow_id, message):
    """
    Sends a message to a grow device
    """
    logger.info(f'Sending AMQP {message} to grow {grow_id}')
    AMQPPublisher(
        'rabbitmq',
        'to_grow/' + str(grow_id),
        message=message
    )
