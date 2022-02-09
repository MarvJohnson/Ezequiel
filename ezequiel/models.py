from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser):
  pass

class DirectMessage(models.Model):
  users = models.ManyToManyField(
    User,
    related_name='direct_messages'
  )

class Message(models.Model):
  sender = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
  )

  text = models.TextField(max_length=1000, null=True)

  replies = models.ForeignKey(
    'self',
    on_delete=models.CASCADE,
    related_name='message_replies',
    blank=True,
    null=True
  )

  messages = models.ForeignKey(
    DirectMessage,
    on_delete=models.CASCADE,
    related_name='messages',
    blank=True,
    null=True
  )

  def __str__(self):
    return f"{self.sender.username} | {self.text}"