from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
  pass

class DirectMessages(models.Model):
  participants = models.ManyToManyField(
    User
  )

class Messages(models.Model):
  user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name='sender'
  )

  replies = models.ForeignKey(
    'self',
    on_delete=models.CASCADE,
    related_name='message_replies'
  )

  messages = models.ForeignKey(
    DirectMessages,
    on_delete=models.CASCADE,
    related_name='message_messages'
  )