from django.urls import path

from .views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='user_login'),
]
