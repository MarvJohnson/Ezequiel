from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DirectMessage, Message

# Register your models here.

class UserAdmin(BaseUserAdmin):
  list_display = ('first_name', 'last_name', 'username', 'is_admin',)
  list_filter = ('is_admin',)
  fieldsets = (
    (None, {'fields': ('username', 'password',)}),
    ('Personal info', {'fields': ('first_name', 'last_name',)}),
    ('Permissions', {'fields': ('is_admin',)}),
  )

  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('first_name', 'last_name', 'username', 'password1', 'password2'),
    }),
  )
  search_fields = ('username',)
  ordering = ('username',)
  filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(DirectMessage)
admin.site.register(Message)
admin.site.unregister(Group)