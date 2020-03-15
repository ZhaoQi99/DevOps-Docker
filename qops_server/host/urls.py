from django.urls import path

from .views import HostView
urlpatterns = [
    path('', HostView.as_view(), name='user_login'),
]
