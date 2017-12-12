from datetime import timedelta

BEAT_SCHEDULE = {
    'update_grow': {
        'channel_name': 'update-grow',
        'schedule': timedelta(milliseconds=500),
        'message': {'key': 'value'}
    },
}
