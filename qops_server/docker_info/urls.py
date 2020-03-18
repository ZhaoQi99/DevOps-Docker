from django.urls import path

from .views import ContainerView, HostImageView, NetworkView, VolumeView

urlpatterns = [
    path('containers/', ContainerView.as_view(), name='host_containers'),
    path('images/', HostImageView.as_view(), name='host_images'),
    path('volumes/', VolumeView.as_view(), name='host_volumes'),
    path('networks/', NetworkView.as_view(), name='host_networks')
]
