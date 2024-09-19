from django.shortcuts import render
from rest_framework import generics

from chat.models import Message
from chat.serializers import MessageSerializer

# Create your views here.

# This view allows you to list the messages of a chat with GET and to create new messages with POST
class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    ordering = ('-moment',)

    # filter request results based on project_id
    def get_queryset(self):
        queryset = Message.objects.all()
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return  Message.objects.filter(message_project=project_id)
            
        return queryset