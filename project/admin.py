from django.contrib import admin

from project.models import CustomUser, Notification, Project, Task

# Register your models here.

# Adding models to django admin site
admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Notification)
