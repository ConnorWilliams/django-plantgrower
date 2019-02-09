from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta
import collections
import logging
import functools


logger = logging.getLogger(__name__)

# Three-step guide to making model changes:
#
# 1. Change your models (in models.py).
# 2. Run python manage.py makemigrations to create migrations for those changes
# 3. Run python manage.py migrate to apply those changes to the database.


class Grow(models.Model):
    # The first element in each choices tuple is the actual value to be set on
    # the model, and the second element is the human-readable name.
    GROW_STAGES = (
        ('1', 'Germination'),
        ('2', 'Veg'),
        ('3', 'Flower'),
        ('4', 'Dry'),
        ('5', 'Cure'),
        ('6', 'Complete')
    )
    STATUSES = (
        ('1', 'ACTIVE'),
        ('2', 'COMPLETE'),
        ('3', 'CANCELLED')
    )
    HOUR_VALIDATORS = [
        MaxValueValidator(24),
        MinValueValidator(0)
    ]
    strain = models.CharField(
        max_length=100,
    )
    start_date = models.DateTimeField(
        auto_now_add=True,
    )
    current_stage = models.CharField(
        max_length=20,
        choices=GROW_STAGES,
        default='1',
    )
    stage_switch_date = models.DateTimeField(
        auto_now_add=True,
    )
    veg_light_duration = models.IntegerField(
        validators=HOUR_VALIDATORS,
        default=18
    )
    flower_light_duration = models.IntegerField(
        validators=HOUR_VALIDATORS,
        default=12
    )
    temperature = models.IntegerField(
        default=23
    )
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default='1',
    )

    def __str__(self):
        return '{} started growing on {}'.format(
            self.strain,
            self.start_date
        )

    def time_duration_string(self, delta):
        duration_string = ''
        d = collections.OrderedDict([
            ('weeks', 0),
            ('days', 0),
            ('hours', 0),
            ('minutes', 0),
            ('seconds', 0)
        ])
        d['weeks'], d['days'] = divmod(delta.days, 7)
        d['hours'], rem = divmod(delta.seconds, 3600)
        d['minutes'], d['seconds'] = divmod(rem, 60)

        found_sig_fig = False
        for unit, val in d.items():
            if (val != 0 or found_sig_fig):
                duration_string += ' {0} {1}'.format(val, unit)
                found_sig_fig = True
        return duration_string[1:]

    @property
    def grow_time(self):
        now = timezone.localtime(timezone.now())
        delta = now - self.start_date
        return self.time_duration_string(delta)

    @property
    def stage_time(self):
        now = timezone.localtime(timezone.now())
        delta = now - self.stage_switch_date
        return self.time_duration_string(delta)

    @property
    def light_duration(self):
        if self.current_stage == '2':
            duration = self.veg_light_duration
        elif self.current_stage == '3':
            duration = self.flower_light_duration
        else:
            duration = 0
        return timedelta(hours=duration)

    @property
    def dark_duration(self):
        if self.current_stage == '2':
            duration = 24 - self.veg_light_duration
        elif self.current_stage == '3':
            duration = 24 - self.flower_light_duration
        else:
            duration = 24
        return timedelta(hours=duration)

    @property
    def current_temperature(self):
        temp_sensors = self.sensor_set.filter(category='temperature')
        readings = [
            float(temp_sensor.latest_reading)
            for temp_sensor in temp_sensors
        ]
        if readings:
            logger.debug('Temp readings: {}'.format(readings))
            avg_reading = (
                functools.reduce(lambda x, y: x + y, readings) / len(readings)
            )
            return avg_reading
        else:
            return -1

    @property
    def current_moisture(self):
        moisture_sensors = self.sensor_set.filter(category='moisture')
        readings = [
            float(moisture_sensor.latest_reading)
            for moisture_sensor in moisture_sensors
        ]
        if readings:
            logger.debug('Moisture readings: {}'.format(readings))
            avg_reading = (
                functools.reduce(lambda x, y: x + y, readings) / len(readings)
            )
            return avg_reading
        else:
            return -1

    @property
    def current_humidity(self):
        humidity_sensors = self.sensor_set.filter(category='humidity')
        readings = [
            float(humidity_sensor.latest_reading)
            for humidity_sensor in humidity_sensors
        ]
        if readings:
            logger.debug('Humidity readings: {}'.format(readings))
            avg_reading = (
                functools.reduce(lambda x, y: x + y, readings) / len(readings)
            )
            return avg_reading
        else:
            return -1

    @property
    def switch_countdown(self):
        if self.current_stage not in ['2', '3']:
            return 'a different grow phase'

        current_light_duration = self.light_duration
        lights = Light.objects.filter(grow=self)
        if len(lights) > 0:
            delta = (
                lights[0].next_switch_time -
                timezone.localtime(timezone.now())
            )

            return self.time_duration_string(delta)
        else:
            return "No lights found for this grow."


# When each model in the hierarchy is a model all by itself. Each model corresponds
# to its own database table and can be queried and created individually. The
# inheritance relationship introduces links between the child model and each of its
# parents (via an automatically-created OneToOneField). For example:
class Device(models.Model):    
    RPI_PIN_VALIDATORS = [
        MaxValueValidator(27),
        MinValueValidator(-1)
    ]

    grow = models.ForeignKey(Grow, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pin = models.IntegerField(validators=RPI_PIN_VALIDATORS, blank=True)

    def get_fields(self):
        try:
            return [
                (field.name, field.value_to_string(self))
                for field in Sensor._meta.fields
            ]
        except ValueError:
            return None

# All of the fields of Device will also be available in InputDevice, although the
# data will reside in a different database table.
# If you have a Device that is also a InputDevice, you can get from the Device object
# to the InputDevice object by using the lower-case version of the model name:
# >>> device = Device.objects.get(id=12)
# If p is a InputDevice object, this will give the child class:
# >>> device.inputdevice
class InputDevice(Device):
    INPUT_CATEGORIES = [
        ('temperature', 'temperature'),
        ('humidity', 'humidity'),
        ('moisture', 'moisture')
    ]
    device = models.OneToOneField(
        Device, on_delete=models.CASCADE,
        parent_link=True,
    )
    category = models.CharField(max_length=255, choices=INPUT_CATEGORIES)
    model = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '{}: {} on pin {}'.format(self.name, self.model, self.pin)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def readings(self):
        return Reading.objects.filter(sensor=self)

    @property
    def latest_reading(self):
        return self.readings().latest().value


class OutputDevice(Device):
    OUTPUT_CATEGORIES = [
        ('light', 'light'),
        ('fan', 'fan'),
        ('pump', 'pump')
    ]
    device = models.OneToOneField(
        Device, on_delete=models.CASCADE,
        parent_link=True,
    )
    category = models.CharField(max_length=255, choices=OUTPUT_CATEGORIES)
    turned_on = models.BooleanField(default=False)

    def __str__(self):
        return '{}: {} on pin {}'.format(self.name, self.category, self.pin)


class Light(OutputDevice):
    OUTPUT_CATEGORIES = [
        ('light', 'light')
    ]
    output_device = models.OneToOneField(
        OutputDevice, on_delete=models.CASCADE,
        parent_link=True,
    )
    last_switch_time = models.DateTimeField(auto_now_add=True)
    next_switch_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '{} {} on pin {}. Last switched: {}.'.format(
            self.name, self.category, self.pin, self.last_switch_time
        )
    
    def switch(self, status=None):
        """Switch light device.

        Keyword arguments:
        status -- True if lights should be on, False otherwise
                  (default None - this will just toggle the lights)
        """
        if status is None:
            # Just toggle
            self.turned_on = not self.turned_on
            self.last_switch_time = timezone.localtime(timezone.now())
            self.next_switch_time += self.grow.light_duration if self.turned_on else self.grow.dark_duration
        else:
            # Set with supplied status argument
            if status != self.turned_on:
                # Only update switch time if we actually change status on/off
                self.last_switch_time = timezone.localtime(timezone.now())
                self.next_switch_time += self.grow.light_duration if self.turned_on else self.grow.dark_duration
            self.turned_on = status
        self.save()


class Reading(models.Model):
    sensor = models.ForeignKey(InputDevice, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        get_latest_by = 'id'

    def __str__(self):
        return '{}: {}'.format(self.sensor, self.value)

    def get_fields(self):
        try:
            return [
                (field.name, field.value_to_string(self))
                for field in Reading._meta.fields
            ]
        except ValueError:
            return None
