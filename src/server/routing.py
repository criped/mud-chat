from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('mud/', consumers.MUDConsumer.as_asgi()),
]
