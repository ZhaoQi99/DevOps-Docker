from django.urls import path

from .views import LogView

urlpatterns = [
    path('logs/', LogView.as_view(), name='logs'),
]
