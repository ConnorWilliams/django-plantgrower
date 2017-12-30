from datetime import timedelta

BEAT_SCHEDULE = {
    'send_grow_information': {
        'channel_name': 'send-grow-information',
        'schedule': timedelta(seconds=1),
        'message': {}
    },
    'check_light_status': {
        'channel_name': 'check-light-status',
        'schedule': timedelta(seconds=10),
        'message': {}
    },
    'check_light_time': {
        'channel_name': 'check-light-time',
        'schedule': timedelta(seconds=10),
        'message': {}
    },
    'check_temperature': {
        'channel_name': 'check-temperature',
        'schedule': timedelta(seconds=5),
        'message': {}
    },
}
