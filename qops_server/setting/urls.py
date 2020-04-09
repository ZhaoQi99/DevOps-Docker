from django.urls import path

from .views import SettingView

urlpatterns = [
    path('setting/', SettingView.as_view(), name='settings'),
]
