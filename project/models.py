from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_save

# Create your models here.

# application users class
class CustomUser(AbstractUser):

    # subclass to assign their types to different users
    class UserType(models.TextChoices):
        ADMIN = 'ADM', 'Administrator'
        MEMBER = 'MBR', 'Member'

    username = models.CharField(max_length=15, unique=True) # there can only be a username once
    user_type = models.CharField(max_length=3, choices=UserType.choices, default=UserType.ADMIN)


# This class represents the projects that will be managed on the platform
class Project(models.Model):
    label = models.CharField(max_length=100)
    creation_date = models.DateField(auto_now_add=True) # the creation date of the object will be automatically added to this field
    description = models.TextField()


# This class represents the tasks that will be created on the platform
class Task(models.Model):

    # This subclass allows you to define the priority level of tasks
    class TaskPriority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MDM', 'Medium'
        HIGH = 'HGH', 'High'

    # This subclass allows you to define the progression level of tasks
    class TaskStatus(models.TextChoices):
        SCHEDULED = 'SCD', 'Scheduled'
        PROGRESS = 'PRG', 'In progress'
        DONE = 'DNE', 'Done'

    task_author = models.ForeignKey(CustomUser, related_name='task_author', on_delete=models.DO_NOTHING, 
                                    limit_choices_to={'user_type': CustomUser.UserType.ADMIN}) # the last paramter limit the values of this field to admins only
    task_project = models.ForeignKey(Project, related_name="task_project", on_delete=models.CASCADE)
    task_assignees = models.ManyToManyField(CustomUser, related_name="task_assignees")
    label = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    task_priority = models.CharField(max_length=3, choices=TaskPriority.choices, default=TaskPriority.LOW)
    task_status = models.CharField(max_length=3, choices=TaskStatus.choices, default=TaskStatus.SCHEDULED)


# This class represents the notifications that will be sent to notify users of changes on the platform
class Notification(models.Model):

    # this subcalss allows you to define the contexts of the notification sending
    class NotificationType(models.TextChoices):
        TASK_ASSIGNATION = 'ASG', 'Task assignation'
        CHAT = 'CHT', 'Chat'
        TASK_DEADLINE = 'DLN', 'Task deadline'

    notification_project = models.ForeignKey(Project, related_name='notification_project', on_delete=models.CASCADE)
    notification_receiver = models.ForeignKey(CustomUser, related_name='notification_receiver', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    

# password encryptation
@receiver(pre_save, sender=CustomUser)
def password_validation(sender, instance, **kwargs):
    if not instance.is_superuser:
        if not instance.pk:
            instance.set_password(instance.password)
        else:
            original = CustomUser.objects.get(pk=instance.pk)
            print('Old object - old password')
            if instance.password != original.password:
                instance.set_password(instance.password)
