import pytest

from .models import Grow


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


@pytest.mark.django_db
class TestGrowModel(object):
    def test_new_grow_is_active(self):
        grow = create_grow('', 1, 1, 1, 1)
        assert grow.status == 1
