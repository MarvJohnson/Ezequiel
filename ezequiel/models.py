from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager, BaseUserManager
from django.conf import settings

# Create your models here.

class UserManager(UserManager, BaseUserManager):
  def create_user(self, first_name, last_name, username, password=None):
    user = self.model(
      first_name=first_name,
      last_name=last_name,
      username=username
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, first_name, last_name, username, password=None):
    user = self.create_user(
      first_name=first_name,
      last_name=last_name,
      username=username,
      password=password
    )

    user.is_admin = True
    user.save(using=self._db)
    return user

class User(AbstractBaseUser):
  username = models.CharField(max_length=200, unique=True)
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['first_name', 'last_name']

  objects = UserManager()
  
  def __str__(self):
    return f'{self.username} | {self.first_name}'

  def has_perm(self, perm, obj=None):
    return True

  def has_module_perms(self, app_label):
    return True

  @property
  def is_staff(self):
    return self.is_admin

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