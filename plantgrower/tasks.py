# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from plantgrower.models import Grow
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
