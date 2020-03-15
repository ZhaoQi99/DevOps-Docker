from channels.routing import ProtocolTypeRouter, URLRouter

from consumer import routing

application = ProtocolTypeRouter({'websocket': URLRouter(routing.websocket_urlpatterns)})
