# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 22:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantgrower', '0002_auto_20171123_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='grow',
            name='status',
            field=models.CharField(choices=[('1', 'ACTIVE'), ('2', 'COMPLETE'), ('3', 'CANCELLED')], default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='grow',
            name='current_stage',
            field=models.CharField(choices=[('1', 'Germination'), ('2', 'Veg'), ('3', 'Flower'), ('4', 'Chop'), ('5', 'Cure'), ('6', 'Complete')], default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='grow',
            name='last_light_switch',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
