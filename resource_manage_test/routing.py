# mysite/routing.py
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import store.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # 'websocket': AuthMiddlewareStack(
    #     URLRouter(
    #         chat.routing.websocket_urlpatterns
    #     )
    # ),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns+
            store.routing.websocket_urlpatterns
        )
    ),
})