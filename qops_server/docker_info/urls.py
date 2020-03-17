from django.urls import path

from .views import ContainerView

urlpatterns = [
    path('containers/', ContainerView.as_view(), name='containers'),
]
