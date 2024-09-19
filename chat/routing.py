from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from chat.consumers import ChatConsumer

# websocket url for real-time communication
websocket_urlpatterns = [
    re_path(r'chat/', ChatConsumer.as_asgi()),
]
