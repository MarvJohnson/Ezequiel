from django.urls import path, re_path, include
from . import views

urlpatterns = [
  path('remove_direct_message/<int:pk>', views.DirectMessageDetail.as_view(), name='remove_direct_message'),
  re_path(r'^.*\/?$', views.vue_render, name='vue_rener'),
]