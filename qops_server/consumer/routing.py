from django.urls import path

from consumer.consumers import SSHConsumer

websocket_urlpatterns = [
    path('ws/ssh/<str:token>/<int:id>/', SSHConsumer),
]
