from django.urls import path

from .views import SettingView

urlpatterns = [
    path('', SettingView.as_view(), name='settings'),
]
