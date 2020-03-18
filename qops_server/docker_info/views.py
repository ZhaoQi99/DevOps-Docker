from django.core.cache import cache
from django.utils import timezone

from host.models import Host
from utils.api import APIView
# from django_redis import get_redis_connection
from utils.docker import Docker
from utils.exceptions import DockerPortNotSet, HostDoesNotExist

from .serializers import ListDockerInfoSerializer


class ContainerView(APIView):
    def post(self, request):
        serializer = ListDockerInfoSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        host_id = serializer.validated_data['host_id']
        refresh = serializer.validated_data['refresh']
        host = Host.objects.filter(pk=host_id).first()
        if not host:
            raise HostDoesNotExist
        if host.docker_port is None:
            raise DockerPortNotSet
        key = f'host:{host_id}:containers'
        result = cache.get(key)
        if (not result) or (refresh is True):
            docker = Docker(url=host.get_docker_url())
            result = {
                'list': docker.container_list(),
                'datetime': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S.%f')
            }
            cache.set(key, result, timeout=20)
        return self.success(result)


class HostImageView(APIView):
    def post(self, request):
        serializer = ListDockerInfoSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        host_id = serializer.validated_data['host_id']
        refresh = serializer.validated_data['refresh']
        host = Host.objects.filter(pk=host_id).first()
        if not host:
            raise HostDoesNotExist
        if host.docker_port is None:
            raise DockerPortNotSet
        key = f'host:{host_id}:images'
        result = cache.get(key)
        if (not result) or (refresh is True):
            docker = Docker(url=host.get_docker_url())
            result = {
                'list': docker.image_list(),
                'datetime': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S.%f')
            }
            cache.set(key, result, timeout=60)
        return self.success(result)


class VolumeView(APIView):
    def post(self, request):
        serializer = ListDockerInfoSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        host_id = serializer.validated_data['host_id']
        refresh = serializer.validated_data['refresh']
        host = Host.objects.filter(pk=host_id).first()
        if not host:
            raise HostDoesNotExist
        if host.docker_port is None:
            raise DockerPortNotSet
        key = f'host:{host_id}:volumes'
        result = cache.get(key)
        if (not result) or (refresh is True):
            docker = Docker(url=host.get_docker_url())
            result = {
                'list': docker.volume_list(),
                'datetime': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S.%f')
            }
            cache.set(key, result, timeout=100)
        return self.success(result)


class NetworkView(APIView):
    def post(self, request):
        serializer = ListDockerInfoSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        host_id = serializer.validated_data['host_id']
        refresh = serializer.validated_data['refresh']
        host = Host.objects.filter(pk=host_id).first()
        if not host:
            raise HostDoesNotExist
        if host.docker_port is None:
            raise DockerPortNotSet
        key = f'host:{host_id}:networks'
        result = cache.get(key)
        if (not result) or (refresh is True):
            docker = Docker(url=host.get_docker_url())
            result = {
                'list': docker.network_list(),
                'datetime': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S.%f')
            }
            cache.set(key, result, timeout=100)
        return self.success(result)
