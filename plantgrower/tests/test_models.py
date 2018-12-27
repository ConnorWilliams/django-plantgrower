import datetime
from django.test import TestCase
from django.utils import timezone
from plantgrower.models import Grow
from datetime import timedelta
import unittest.mock as mock
import pytz

import pprint
pp = pprint.PrettyPrinter(indent=4)
# pp.pprint()

# Make now() a constant
NOW_FOR_TESTING = datetime.datetime(2017, 11, 27, 10, 0, 0, 0, pytz.UTC)


# This is the function that replaces django.utils.timezone.now()
def mocked_now():
    return NOW_FOR_TESTING


def create_grow(strain, veg_light, flower_light):
    """
    Create a grow with the given parameters
    """
    return Grow.objects.create(
        strain=strain,
        veg_light_duration=veg_light,
        flower_light_duration=flower_light,
    )


class TestGrowModel(TestCase):
    def test_new_grow_is_active(self):
        grow = create_grow('', 1, 1)
        self.assertEqual(
            grow.status,
            '1'
        )

    def test_grow_string(self):
        strain_name = 'My strain'
        grow = create_grow(strain_name, 1, 1)
        self.assertIn(
            "{} started growing on".format(strain_name),
            str(grow)
        )

    def test_time_duration_string(self):
        grow = create_grow('', 1, 1)
        delta = timedelta(days=3, hours=2)
        self.assertEqual(
            grow.time_duration_string(delta),
            "3 days 2 hours 0 minutes 0 seconds"
        )
        self.assertTrue(True)

    @mock.patch('django.utils.timezone.now', side_effect=mocked_now)
    def test_now_mock(self, *args):
        now = timezone.localtime(timezone.now())
        self.assertEqual(
            now,
            NOW_FOR_TESTING
        )
        self.assertEqual(
            mocked_now(),
            NOW_FOR_TESTING
        )
        self.assertTrue(True)

    @mock.patch('django.utils.timezone.now', side_effect=mocked_now)
    def test_grow_time(self, *args):
        grow = create_grow('NL', 1, 1)
        grow.start_date = grow.start_date - timedelta(hours=1)
        self.assertEqual(
            grow.grow_time,
            '1 hours 0 minutes 0 seconds'
        )
        self.assertTrue(True)

    @mock.patch('django.utils.timezone.now', side_effect=mocked_now)
    def test_stage_time(self, *args):
        grow = create_grow('', 1, 1)
        grow.stage_switch_date = grow.stage_switch_date - timedelta(
            hours=2,
            minutes=30
        )
        self.assertEqual(
            grow.stage_time,
            '2 hours 30 minutes 0 seconds'
        )
        self.assertTrue(True)

    def test_light_duration(self):
        grow = create_grow('', 1, 2)
        self.assertEqual(
            grow.light_duration,
            0
        )
        grow.current_stage = '2'
        self.assertEqual(
            grow.light_duration,
            1
        )
        grow.current_stage = '3'
        self.assertEqual(
            grow.light_duration,
            2
        )
        grow.current_stage = '4'
        self.assertEqual(
            grow.light_duration,
            0
        )
        self.assertTrue(True)

    def test_dark_duration(self):
        grow = create_grow('', 1, 2)
        self.assertEqual(
            grow.dark_duration,
            24
        )
        grow.current_stage = '2'
        self.assertEqual(
            grow.dark_duration,
            23
        )
        grow.current_stage = '3'
        self.assertEqual(
            grow.dark_duration,
            22
        )
        grow.current_stage = '4'
        self.assertEqual(
            grow.dark_duration,
            24
        )
        self.assertTrue(True)

    def test_switch_countdown(self):
        grow = create_grow('', 1, 2)
        self.assertEqual(
            grow.switch_countdown,
            'a different grow phase'
        )
        grow.current_stage = '2'
        self.assertEqual(
            grow.switch_countdown,
            '22 hours 59 minutes 59 seconds'  # 23 hours
        )
        grow.current_stage = '3'
        self.assertEqual(
            grow.switch_countdown,
            '21 hours 59 minutes 59 seconds'  # 22 hours
        )
        grow.current_stage = '4'
        self.assertEqual(
            grow.switch_countdown,
            'a different grow phase'
        )
        self.assertTrue(True)
