import pytest

from .models import Grow

from django.test import Client
from django.urls import reverse

# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint()


def create_grow(strain, veg_light, veg_dark, flower_light, flower_dark):
    """
    Create a grow with the given parameters
    """
    return Grow.objects.create(
        strain=strain,
        veg_light_duration=veg_light,
        veg_dark_duration=veg_dark,
        flower_light_duration=flower_light,
        flower_dark_duration=flower_light
    )


class TestIndexView(object):
    @pytest.mark.django_db
    def test_no_grows(self):
        """
        If no grows exist, new grow form is displayed.
        """
        self.client = Client()
        response = self.client.get(reverse('plantgrower:index'))
        assert response.status_code == 200
        assert "Strain:" in str(response._container)

    @pytest.mark.django_db
    def test_post(self):
        """
        Test we can post
        """
        self.client = Client()
        self.client.post('/plantgrower/newgrow', {
            'strain': 'NL',
            'veg_light_duration': '1',
            'veg_dark_duration': '1',
            'flower_light_duration': '1',
            'flower_dark_duration': '1'
        })
        assert len(Grow.objects.all()) == 1

    @pytest.mark.django_db
    def test_active_grow(self):
        """
        Active grow is displayed on the index page if exists.
        """
        self.client = Client()
        grow = create_grow('Strain1', 1, 1, 1, 1)
        grow.save()
        response = self.client.get(reverse('plantgrower:index'))
        assert response.request['PATH_INFO'] == '/plantgrower/'


class TestAllGrowsView(object):
    @pytest.mark.django_db
    def test_all_grows(self):
        """
        All grows are displayed on the page
        """
        self.client = Client()
        grow1 = create_grow('Strain1', 1, 1, 1, 1)
        grow1.save()
        grow2 = create_grow('Strain2', 12, 12, 16, 8)
        grow2.save()
        grow3 = create_grow('Strain3', 10, 14, 2, 22)
        grow3.save()
        response = self.client.get(reverse('plantgrower:allgrows'))
        assert str(response._container[0]).count('started growing on') == 3
        assert response.request['PATH_INFO'] == '/plantgrower/allgrows'


class TestEditGrowView(object):
    @pytest.mark.django_db
    def test_editgrow_get(self):
        self.client = Client()
        grow = create_grow('Strain1', 1, 1, 1, 1)
        response = self.client.get(
            reverse('plantgrower:editgrow', args=[grow.id])
        )
        assert response.status_code == 200
        assert "Strain:" in str(response._container)

    @pytest.mark.django_db
    def test_editgrow_post(self):
        self.client = Client()
        grow = create_grow('Strain1', 1, 1, 1, 1)
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
        assert grow.strain == 'NewName'
