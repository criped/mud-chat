import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack

from server import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = ProtocolTypeRouter({
    "websocket": SessionMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
