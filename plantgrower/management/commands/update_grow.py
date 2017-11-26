from channels import Group
from django.core.management.base import BaseCommand
import time
from plantgrower.models import Grow


# The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "Send things to channel."

    # A command must define handle()
    def handle(self, *args, **options):
        grow = Grow.objects.filter(status='1')[0]
        while True:
            Group('stage').send({
               "text": str(grow.stage_time)
            })
            time.sleep(2)
