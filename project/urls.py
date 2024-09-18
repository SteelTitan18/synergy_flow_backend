# this file contains requests routes for the app
from django.urls import path, include
from rest_framework import routers

from project import views

router = routers.SimpleRouter()

# defining the base route for requests
router.register('custom_user', views.CustomUserViewSet, basename="custom_user")
router.register('project', views.ProjectViewSet, basename="project")
router.register('task', views.TaskViewSet, basename="task")
router.register('notification', views.NotificationViewSet, basename='participant')

urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.SigninView.as_view()),     # adding of login route
]
