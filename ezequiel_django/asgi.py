"""
ASGI config for ezequiel_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import ezequiel.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ezequiel_django.settings')

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': AuthMiddlewareStack(
    URLRouter(
      ezequiel.routing.websocket_urlpatterns
    )
  )
})
