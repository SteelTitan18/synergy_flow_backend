from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from chat.consumers import ChatConsumer

# websocket url for real-time communication
websocket_urlpatterns = [
    re_path(r"^ws/chat/(?P<project_id>\d+)/$", ChatConsumer.as_asgi()),  # Captures project_id in the URL
]
