from django.conf.urls import url

from . import views

app_name = 'plantgrower'
urlpatterns = [
    url(
        r'^$',
        views.index,
        name='index'
    ),
    url(
        r'^newgrow$',
        views.new_grow,
        name='newgrow'
    ),
    # url(
    #     r'^/settings/$',
    #     views.SettingsView.as_view(),
    #     name='settings'
    # ),
    # url(
    #     r'^/summary/$',
    #     views.sumary,
    #     name='summary'
    # ),
]
