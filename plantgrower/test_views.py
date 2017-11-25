import pytest

from datetime import datetime
import pytz

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
        # assert response.context['latest_question_list'] == []

    @pytest.mark.django_db
    def test_post(self):
        """
        Test we can post
        """
        self.client = Client()
        response = self.client.post('/plantgrower/newgrow', {
            'strain': 'NL',
            'veg_light_duration': '1',
            'veg_dark_duration': '1',
            'flower_light_duration': '1',
            'flower_dark_duration': '1'
        })
        print(response.status_code)
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
        import pprint
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(vars(response))
        assert str(response._container[0]).count('started growing on') == 3
        assert response.request['PATH_INFO'] == '/plantgrower/allgrows'

    @pytest.mark.django_db
    def test_date_change(self):
        """
        You should not be able to set the start_date.
        """
        start_date = datetime(2000, 1, 1, 1, 1, 1, 1, pytz.UTC)
        grow = Grow.objects.create(
            strain='',
            veg_light_duration=1,
            veg_dark_duration=1,
            flower_light_duration=1,
            flower_dark_duration=1,
            start_date=start_date
        )
        grow.save()
        assert len(Grow.objects.all()) == 1
        assert not Grow.objects.filter(start_date=start_date)
