import logging
import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)

GROUP_COUNTER = {}


class GrowConsumer(JsonWebsocketConsumer):
    groups = ["all_grows"]

    def connect(self):
        self.accept()
        logger.warning(self.scope['path'])
        _url = self.scope['path'][1:-1].replace('/', '-')
        try:
            PeriodicTask.objects.get(name=_url)
        except Exception as e:
            logger.info(e)
            schedule, _created = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.SECONDS,
            )
            PeriodicTask.objects.create(
                interval=schedule,
                name=_url,
                task='plantgrower.tasks.send_grow_information',
                args=json.dumps([_url])
            )
        async_to_sync(self.channel_layer.group_add)(_url, self.channel_name)
        GROUP_COUNTER[_url] = GROUP_COUNTER.get(_url, 0) + 1
        logger.warning('Someone connected to {}'.format(_url))

    def send_grow(self, content):
        self.send_json(content=content['text'])

    def disconnect(self, close_code):
        # Called when the socket closes
        _url = self.scope['path'][1:-1].replace('/', '-')
        async_to_sync(self.channel_layer.group_discard)(
            _url, self.channel_name
        )
        logger.info('Someone left from {}'.format(_url))
        GROUP_COUNTER[_url] = GROUP_COUNTER[_url] - 1
        if GROUP_COUNTER[_url] == 0:
            try:
                PeriodicTask.objects.get(name=_url).delete()
            except Exception as e:
                logger.error(e)
