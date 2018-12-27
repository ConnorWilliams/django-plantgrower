# Used with channels

# from channels.routing import route
# from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from plantgrower.consumers import GrowConsumer
from django.urls import path

plantgrower_router = URLRouter([
    path("grows/<int:grow_id>/", GrowConsumer)
])
