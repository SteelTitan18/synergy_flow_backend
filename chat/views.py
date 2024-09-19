from django.shortcuts import render
from rest_framework import generics

from chat.models import Message
from chat.serializers import MessageSerializer

# Create your views here.

# This view allows you to list the messages of a chat with GET and to create new messages with POST
class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    ordering = ('-moment',)