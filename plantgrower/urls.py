from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from plantgrower import views


app_name = 'plantgrower'
urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='index'
    ),
    path(
        'newgrow/',
        views.NewGrow.as_view(),
        name='newgrow'
    ),
    path(
        'grows/',
        views.Grows.as_view(),
        name='grows'
    ),
    path(
        'grows/<int:grow_id>/',
        views.GrowControl.as_view(),
        name='growcontrol'
    ),
    path(
        'editgrow/<int:grow_id>/',
        views.EditGrow.as_view(),
        name='editgrow'
    ),
    path(
        'nextstage/<int:grow_id>/',
        views.NextStage.as_view(),
        name='nextstage'
    ),
    path(
        'newinputdevice/<int:grow_id>/',
        views.NewInputDevice.as_view(),
        name='newinputdevice'
    ),
    path(
        'api/grows/',
        views.GrowList.as_view()
    ),
    path(
        'api/grows/<int:pk>/',
        views.GrowDetail.as_view()
    ),
    path(
        'api/inputdevice/',
        views.InputDeviceList.as_view()
    ),
    path(
        'api/inputdevice/<int:pk>/',
        views.InputDeviceDetail.as_view()
    ),
    path(
        'api/outputdevice/',
        views.OutputDeviceList.as_view()
    ),
    path(
        'api/outputdevice/<int:pk>/',
        views.OutputDeviceDetail.as_view()
    ),
    path(
        'api/readings/',
        views.ReadingList.as_view()
    ),
    path(
        'api/readings/<int:pk>/',
        views.ReadingDetail.as_view()
    )
]

urlpatterns = format_suffix_patterns(urlpatterns)
