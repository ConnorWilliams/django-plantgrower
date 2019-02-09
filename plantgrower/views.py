import logging

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils import timezone
from django.db.utils import IntegrityError
from django.views.generic import ListView
from rest_framework import generics
from plantgrower.models import Grow, Device, InputDevice, Reading, OutputDevice, Light
from plantgrower.forms import GrowForm, InputDeviceForm, OutputDeviceForm
from plantgrower.serializers import (
    GrowSerializer,
    InputDeviceSerializer,
    OutputDeviceSerializer,
    ReadingSerializer
)


logger = logging.getLogger(__name__)


class Index(View):
    def get(self, request):
        if Grow.objects.filter(status='1'):
            logger.info("Active grow found")
            return HttpResponseRedirect('/plantgrower/grows')
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


class Grows(ListView):
    model = Grow


class GrowControl(View):
    def get(self, request, grow_id):
        self.grow = get_object_or_404(Grow, pk=grow_id)
        logger.info(self.grow)
        input_devices = self._get_devices(InputDevice)
        output_devices = self._get_devices(OutputDevice)
        return render(
            request,
            'plantgrower/dashboard.html',
            {
                'grow': self.grow,
                'input_devices': input_devices,
                'output_devices': output_devices,
            }
        )
    
    def _get_devices(self, device_type):
        categorized_devices = {}
        try:
            categorized_devices = self._categorize_devices(
                device_type.objects.filter(grow=self.grow)
            )
        except device_type.DoesNotExist as e:
            logger.debug("No devices found.")
            logger.debug(e)
        return categorized_devices
    
    def _categorize_devices(self, devices):
        categorized_devices = {}
        for category in devices.order_by().values_list(
            'category', flat=True
        ).distinct():
            categorized_devices[category] = \
                devices.filter(category=category)
        return categorized_devices


class NewInputDevice(View):
    def get(self, request, grow_id):
        grow = get_object_or_404(Grow, pk=grow_id)
        input_device = InputDevice(
            grow=grow
        )
        form = InputDeviceForm(instance=input_device)
        return render(
            request,
            'plantgrower/inputdevice_form.html',
            {'form': form, 'grow': grow}
        )

    def post(self, request, grow_id):
        grow = get_object_or_404(Grow, pk=grow_id)
        input_device = InputDevice(
            grow=grow
        )
        form = InputDeviceForm(request.POST, instance=input_device)
        if form.is_valid():
            form.save()
            return redirect('plantgrower:growcontrol', grow_id=grow_id)
        else:
            raise Http404("Cannot save input device.")


class NewOutputDevice(View):
    def get(self, request, grow_id):
        grow = get_object_or_404(Grow, pk=grow_id)
        output_device = OutputDevice(
            grow=grow
        )
        form = OutputDeviceForm(instance=output_device)
        return render(
            request, 'plantgrower/outputdevice_form.html', {'form': form, 'grow': grow}
        )

    def post(self, request, grow_id):
        self.grow = get_object_or_404(Grow, pk=grow_id)
        output_device = OutputDevice(
            grow=self.grow
        )
        form = OutputDeviceForm(request.POST, instance=output_device)
        if form.is_valid():
            self._create_output_device_from_form(form)
            return redirect('plantgrower:growcontrol', grow_id=self.grow.id)
        else:
            raise Http404("Form is not valid. Did not save.")
    
    def _create_output_device_from_form(self, form):
        output_device = form.save()
        if output_device.category == 'light':
            self._create_light_from_outputdevice(output_device)
        return output_device

    def _create_light_from_outputdevice(self, output_device):
        light = Light(
            name=output_device.name,
            pin=output_device.pin,
            category=output_device.category,
            grow = self.grow,
            output_device = output_device
        )
        light.save()
        return light



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
            return redirect('plantgrower:growcontrol', grow_id=grow_id)

        return render(
            request, 'plantgrower/editgrow.html', {'form': form, 'grow': grow}
        )


class NextStage(View):
    def get(self, request, grow_id):
        grow = get_object_or_404(Grow, pk=grow_id)
        if grow.current_stage == '6':
            return redirect('plantgrower:growcontrol', grow_id=grow_id)
        
        grow.current_stage = str(int(grow.current_stage) + 1)
        grow.stage_switch_date = timezone.localtime(timezone.now())
        # If finished, change status to complete.
        if grow.current_stage == '6':
            grow.status = '2'
        # If turning to a stage with no light, turn em off.
        if grow.current_stage in ['1', '4', '5', '6']:
            [
                light.switch(False) for 
                light in Light.objects.filter(grow=grow)
            ]
        # If turning to a stage with light, turn em on.
        if grow.current_stage in ['2', '3']:
            [
                light.switch(True) for 
                light in Light.objects.filter(grow=grow)
            ]
        grow.save()
        return redirect('plantgrower:growcontrol', grow_id=grow_id)


class GrowList(generics.ListCreateAPIView):
    queryset = Grow.objects.all()
    serializer_class = GrowSerializer


class GrowDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grow.objects.all()
    serializer_class = GrowSerializer


class InputDeviceList(generics.ListCreateAPIView):
    queryset = InputDevice.objects.all()
    serializer_class = InputDeviceSerializer


class InputDeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InputDevice.objects.all()
    serializer_class = InputDevice


class OutputDeviceList(generics.ListCreateAPIView):
    queryset = OutputDevice.objects.all()
    serializer_class = OutputDeviceSerializer


class OutputDeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OutputDevice.objects.all()
    serializer_class = OutputDeviceSerializer


class ReadingList(generics.ListCreateAPIView):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer


class ReadingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
