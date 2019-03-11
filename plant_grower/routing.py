# Used with channels

# from channels.routing import route
# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from plantgrower.routing import plantgrower_router

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path('/', plantgrower_router),
    ])
})
