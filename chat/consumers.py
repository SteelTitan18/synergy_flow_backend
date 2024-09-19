import json
import time

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, AsyncToSync

from project.models import Project

from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):

    # connection to chat room
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["project_id"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    # disconnect from chat room
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        content = text_data_json["content"]
        username = text_data_json["username"]
        moment = text_data_json["moment"]

        room = self.room_name

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": content, "username": username, "moment": moment},
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        moment = event["moment"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "moment": moment, "username": username}))

    @sync_to_async
    def save_message(self, username, message):
        Message.objects.create(sender=username, content=message, project=Project.objects.get(pk=self.room_name))
