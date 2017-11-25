import logging

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Grow
from .forms import GrowForm
from .gpio import lights_on, fans_on

logger = logging.getLogger(__name__)


class Index(View):
    def get(self, request):
        if Grow.objects.filter(status='1'):
            logger.info("Active grow found")
            return HttpResponseRedirect('/plantgrower/currentgrow')
        else:
            logger.info("No active grows")
            return HttpResponseRedirect('/plantgrower/newgrow')


class NewGrow(View):
    def get(self, request):
        if not Grow.objects.filter(status='1'):
            form = GrowForm()
        else:
            logger.info("Showing active grow")
            return HttpResponseRedirect('/plantgrower/')
        return render(request, 'plantgrower/newgrow.html', {'form': form})

    def post(self, request):
        form = GrowForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/plantgrower/')

        return render(request, 'plantgrower/newgrow.html', {'form': form})


class CurrentGrow(View):
    def get(self, request):
        grow = Grow.objects.filter(status='1')[0]
        lights = {
            'on_duration': grow.light_duration,
            'off_duration': 24 - grow.light_duration,
            'status': 'ON' if lights_on() else 'OFF',
            'switch_countdown': grow.switch_countdown
        }
        fans = {
            'status': 'ON' if fans_on() else 'OFF',
        }
        return render(
            request,
            'plantgrower/currentgrow.html',
            {
                'grow': grow,
                'lights': lights,
                'fans': fans,
            }
        )


class EditGrow(View):
    def get(self, request, grow_id):
        grow = get_object_or_404(Grow, pk=grow_id)
        form = GrowForm(instance=grow)
        return render(
            request, 'plantgrower/editgrow.html', {'form': form, 'grow': grow}
        )

    def post(self, request, grow_id):
        grow = get_object_or_404(Grow, pk=grow_id)
        form = GrowForm(request.POST, instance=grow)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/plantgrower/')

        return render(
            request, 'plantgrower/editgrow.html', {'form': form, 'grow': grow}
        )


class AllGrows(View):
    def get(self, request):
        grows = Grow.objects.all()
        output = '</br>'.join([str(grow) for grow in grows])
        return HttpResponse(output)
