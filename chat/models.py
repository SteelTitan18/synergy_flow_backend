from django.db import models

from project.models import Project

# Create your models here.
class Message(models.Model):
    content = models.TextField()
    message_project = models.ForeignKey(Project, related_name='message_project', on_delete=models.CASCADE)      # <Banner title={"Liste des projets"} />
    sender = models.CharField(max_length=15)    # the username of the sender
    moment = models.DateTimeField(auto_now_add=True)
