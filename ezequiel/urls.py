from django.urls import path, re_path, include
from . import views

urlpatterns = [
  re_path(r'^.*\/?$', views.vue_render, name='vue_rener')
]