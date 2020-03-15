from django.urls import path

from .views import HostView, web_ssh

urlpatterns = [
    path('', HostView.as_view(), name='hosts'),
    path('ssh/<int:h_id>/', web_ssh),
]
