from django.urls import path

from consumer.consumers import SSHConsumer

websocket_urlpatterns = [
    path('api/ws/ssh/<str:token>/<int:id>/', SSHConsumer),
]
