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
    url(
        r'^editgrow/(?P<grow_id>[0-9]+)/$',
        views.edit_grow,
        name='editgrow'
    ),
    url(
        r'^allgrows$',
        views.all_grows,
        name='allgrows'
    )
]
