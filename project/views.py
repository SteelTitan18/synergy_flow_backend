import re
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

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
    

class AssigneesOrAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return request.user in obj.task_assignees.all() or request.user.user_type == 'ADM'
    

# admin user permission class
class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'ADM'


# This function generates token and refresh_token for authentication
def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

# This is the view which implements the authentication
class SigninView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    

    def post(self, request, *args, **kwargs):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' # email regular expression
        username = request.data.get("username", None)       # get credentials from the request
        password = request.data.get("password", None)

        # since the user can log in either by email or by username, it is necessary to check 
        # which of the 2 was used and retrieve the user based on that
        try:
            if re.match(email_regex, username):
                user = CustomUser.objects.get(email=username)
            else:
                user = CustomUser.objects.get(username = username)

            auth = user.check_password(password)    # check if the password given is the same as                                    # the user found password

            if auth:
                # if the user is authenticated, a response will be sent to 
                # the frontend with this following payload
                token_data = get_tokens_for_user(user)
                token = token_data["access"]
                refresh = token_data["refresh"]
                response = Response(
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "firstname": user.first_name,
                        "lastname": user.last_name,
                        "token": token,
                        "refresh": refresh,
                        'type': user.user_type
                    }
                )
                return response

            else: # if the auth is false, the the passsword is wrong
                return Response({'error': 'Incorrect password'})
        except: # if the user is not found, the user must correct it's email or username
            return Response({'message': 'User not found'})


# This class allows you to implement the execution of each of the requests 
# (POST, GET, DELETE, PUT) on each of the classes of the application
class CustomUserViewSet(ModelViewSet):
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
    
    def get_queryset(self):
        queryset = CustomUser.objects.all()
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return  Project.objects.get(pk=project_id).assignees.all()
            
        return queryset
    

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    fields = '__all__'


    def get_permissions(self):
        # members are just allowed to do GET method
        if self.action == 'list' or self.action == 'retrieve':
            return [MemberPermission()]
        
        return [AdminPermission(), ]


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    fields = '__all__'

    def get_permissions(self):
        # in the case of tasks, only the admins can do POST and DELETE, 
        # members can do GET requests and only assignees users or and admin can do an PUT request
        if self.action == 'update' or  self.action == 'retrieve':
            return [ AssigneesOrAdminPermission()]
        elif self.action == 'list':
            return [MemberPermission()]
        
        return [AdminPermission()]
    
    def get_queryset(self):
        queryset = Task.objects.all()
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return  Task.objects.filter(task_project=project_id)
            
        return queryset
        

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    fields = '__all__'

    def get_permissions(self):       
        return [MemberPermission(), ]