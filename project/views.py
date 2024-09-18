from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, BasePermission

from project.models import CustomUser, Notification, Project, Task
from project.serializers import CustomUserSerializer, NotificationSerializer, ProjectSerializer, TaskSerializer

# Create your views here.

# all users permissions class
class MemberPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    

class ProfilePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user
    

class AssigneesPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return request.user in obj.assignees.all()
    

# admin user permission class
class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'ADM'


# This class allows you to implement the execution of each of the requests 
# (POST, GET, DELETE, PUT) on each of the classes of the application
class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    fields = '__all__'

    # this class define permissions for different types of requests
    def get_permissions(self):
        # in the case of users, only the admins can do POST and DELETE, 
        # members can do GET requests and only the user or and admin can do an PUT request
        if self.action == 'update':
            return [ProfilePermission(), AdminPermission()]
        elif self.action == 'list':
            return [MemberPermission()]
        
        return [AdminPermission(), ]
    

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    fields = '__all__'


    def get_permissions(self):
        # members are just allowed to do GET method

        if self.action == 'list':
            return [MemberPermission()]
        
        return [AdminPermission(), ]


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    fields = '__all__'

    def get_permissions(self):
        # in the case of tasks, only the admins can do POST and DELETE, 
        # members can do GET requests and only assignees users or and admin can do an PUT request
        if self.action == 'update':
            return [AssigneesPermission(), AdminPermission()]
        elif self.action == 'list':
            return [MemberPermission()]
        
        return [AdminPermission(), ]
        

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    fields = '__all__'

    def get_permissions(self):       
        return [MemberPermission(), ]