from datetime import timedelta

BEAT_SCHEDULE = {
    'send_grow_information': {
        'channel_name': 'send-grow-information',
        'schedule': timedelta(milliseconds=500),
        'message': {}
    },
    'monitor_grow': {
        'channel_name': 'monitor-grow',
        'schedule': timedelta(seconds=60),
        'message': {}
    },
}
