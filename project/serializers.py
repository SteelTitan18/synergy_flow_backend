# this file contains the data format on the different app's requests

from project.models import CustomUser, Notification, Project, Task
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # definition of the class according to which the data will be formatted
        fields = '__all__'  # selection of the fields that will be formatted. In this case all of them


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        