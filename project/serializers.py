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
    # add project complete data to task payload
    task_project = ProjectSerializer(read_only=True)
    project_id = serializers.IntegerField(write_only=True)
    assignees = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all(), write_only=True)

    def create(self, validated_data):
        project = Project.objects.get(pk=validated_data.pop('project_id'))
        assignees = validated_data.pop('task_assignees', [])
        
        # Create the task instance
        task = Task.objects.create(task_project=project, **validated_data)
        
        # Set the many-to-many relationship
        if assignees:
            task.task_assignees.set(assignees)
        
        return task

    class Meta:
        model = Task
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        