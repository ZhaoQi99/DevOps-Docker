from django.urls import path

from .views import ContainerView, HostImageView

urlpatterns = [
    path('containers/', ContainerView.as_view(), name='host_containers'),
    path('images/', HostImageView.as_view(), name='host_images')
]
