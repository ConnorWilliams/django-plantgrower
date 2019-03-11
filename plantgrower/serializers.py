from rest_framework import serializers
from plantgrower.models import Grow, InputDevice, OutputDevice, Reading


class GrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grow
        depth = 1
        fields = (
            'id',
            'strain',
            'start_date',
            'current_stage',
            'stage_switch_date',
            'veg_light_duration',
            'flower_light_duration',
            'temperature',
            'humidity',
            'status',
            'grow_time',
            'stage_time',
            'current_temperature',
            'current_moisture',
            'current_humidity',
            'switch_countdown'
        )


class InputDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputDevice
        depth = 1
        fields = (
            'id',
            'grow',
            'name',
            'pin',
            'category',
            'model',
            'latest_reading'
        )


class OutputDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputDevice
        depth = 1
        fields = (
            'id',
            'grow',
            'name',
            'pin',
            'category',
            'last_switch_time',
            'system_status',
            'user_status'
        )


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        depth = 1
        fields = (
            'sensor',
            'value',
            'date'
        )
