from django.conf.urls import url

from . import views

app_name = 'plantgrower'
urlpatterns = [
    url(
        r'^$',
        views.Index.as_view(),
        name='index'
    ),
    url(
        r'^newgrow$',
        views.NewGrow.as_view(),
        name='newgrow'
    ),
    url(
        r'^editgrow/(?P<grow_id>[0-9]+)/$',
        views.EditGrow.as_view(),
        name='editgrow'
    ),
    url(
        r'^allgrows$',
        views.AllGrows.as_view(),
        name='allgrows'
    ),
]
