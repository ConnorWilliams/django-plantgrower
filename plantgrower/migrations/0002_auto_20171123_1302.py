# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 19:02
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantgrower', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strain', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('current_stage', models.CharField(choices=[(1, 'Germination'), (2, 'Veg'), (3, 'Flower'), (4, 'Chop'), (5, 'Cure'), (6, 'Complete')], default=1, max_length=100)),
                ('veg_light_duration', models.IntegerField(validators=[django.core.validators.MaxValueValidator(24), django.core.validators.MinValueValidator(0)])),
                ('veg_dark_duration', models.IntegerField(validators=[django.core.validators.MaxValueValidator(24), django.core.validators.MinValueValidator(0)])),
                ('flower_light_duration', models.IntegerField(validators=[django.core.validators.MaxValueValidator(24), django.core.validators.MinValueValidator(0)])),
                ('flower_dark_duration', models.IntegerField(validators=[django.core.validators.MaxValueValidator(24), django.core.validators.MinValueValidator(0)])),
                ('last_light_switch', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]