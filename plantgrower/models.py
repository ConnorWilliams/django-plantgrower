import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

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
        ('4', 'Chop'),
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
        default=1,
    )
    veg_light_duration = models.IntegerField(validators=HOUR_VALIDATORS)
    veg_dark_duration = models.IntegerField(validators=HOUR_VALIDATORS)
    flower_light_duration = models.IntegerField(validators=HOUR_VALIDATORS)
    flower_dark_duration = models.IntegerField(validators=HOUR_VALIDATORS)
    last_light_switch = models.DateTimeField(
        auto_now_add=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default=1,
    )

    def __str__(self):
        return "{} started growing on {}".format(
            self.strain,
            self.start_date
        )

    def started_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.start_date <= now

    def grow_time(self):
        now = timezone.now()
        return now - self.start_date
