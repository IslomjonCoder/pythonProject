import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import cafe.routing
from config import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(
        URLRouter(
            cafe.routing.websocket_urlpatterns
        )
    )),
})
