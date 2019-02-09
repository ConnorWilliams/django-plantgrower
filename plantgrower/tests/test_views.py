from django.test import TestCase
from django.test import Client
from django.urls import reverse

from plantgrower.models import Grow, InputDevice, Reading, OutputDevice, Light
from plantgrower.views import NewOutputDevice

import pprint
pp = pprint.PrettyPrinter(indent=4)
# pp.pprint()


def create_grow(strain, veg_light, flower_light):
    """
    Create a grow with the given parameters
    """
    return Grow.objects.create(
        strain=strain,
        veg_light_duration=veg_light,
        flower_light_duration=flower_light,
    )


class TestIndexView(TestCase):
    def test_no_grows(self):
        """
        If no grows exist, new grow form is displayed.
        """
        self.client = Client()
        response = self.client.get(reverse('plantgrower:index'))
        self.assertEqual(
            response.status_code,
            302
        )
        self.assertIn(
            '/plantgrower/newgrow',
            response._headers['location']
        )

    def test_post(self):
        """
        Test we can post
        """
        self.client = Client()
        response = self.client.post('/plantgrower/newgrow/', {
            'strain': 'NL',
            'veg_light_duration': '1',
            'flower_light_duration': '1',
            'temperature': '24',
            'humidity': '62'
        })
        self.assertEqual(
            response.status_code,
            302
        )
        self.assertEqual(
            len(Grow.objects.all()),
            1
        )

    def test_active_grow(self):
        """
        Active grow is displayed on the index page if exists.
        """
        self.client = Client()
        grow = create_grow('Strain1', 1, 1)
        grow.save()
        response = self.client.get(reverse('plantgrower:index'))
        self.assertEqual(
            response.request['PATH_INFO'],
            '/plantgrower/'
        )


class TestAllGrowsView(TestCase):
    def test_all_grows(self):
        """
        All grows are displayed on the page
        """
        self.client = Client()
        grow1 = create_grow('Strain1', 1, 1)
        grow1.save()
        grow2 = create_grow('Strain2', 12, 12)
        grow2.save()
        grow3 = create_grow('Strain3', 10, 14)
        grow3.save()
        response = self.client.get(reverse('plantgrower:grows'))
        self.assertEqual(
            str(response._container[0]).count('Strain'),
            3
        )
        self.assertEqual(
            response.request['PATH_INFO'],
            '/plantgrower/grows/'
        )


class TestEditGrowView(TestCase):
    def test_editgrow_get(self):
        self.client = Client()
        grow = create_grow('Strain1', 1, 1)
        response = self.client.get(
            reverse('plantgrower:editgrow', args=[grow.id])
        )
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertIn(
            "Strain",
            str(response._container)
        )

    def test_editgrow_post(self):
        self.client = Client()
        grow = create_grow('Strain1', 1, 1)
        self.client.post(
            reverse('plantgrower:editgrow', args=[grow.id]), {
                'strain': 'NewName',
                'veg_light_duration': '2',
                'veg_dark_duration': '2',
                'flower_light_duration': '2',
                'flower_dark_duration': '2'
            }
        )
        grow = Grow.objects.get(pk=grow.id)
        self.assertEqual(
            grow.strain,
            'Strain1'
        )

class TestNewOutputDeviceView(TestCase):
    def test_post(self):
        """
        All grows are displayed on the page
        """
        self.client = Client()
        grow = Grow('', 12, 12)
        response = self.client.post('/plantgrower/newoutputdevice/1', {
            'name': 'Test',
            'pin': '10',
            'category': 'fan',
        })
        # self.assertEqual(
        #     response.status_code,
        #     302
        # )
        self.assertEqual(
            len(OutputDevice.objects.all()),
            1
        )
        response = self.client.post('/plantgrower/newoutputdevice/1', {
            'name': 'Test',
            'pin': '11',
            'category': 'light',
        })
        # self.assertEqual(
        #     response.status_code,
        #     302
        # )
        self.assertEqual(
            len(OutputDevice.objects.all()),
            2
        )
        self.assertEqual(
            len(Light.objects.all()),
            1
        )
        