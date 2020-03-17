import docker
from django.template.defaultfilters import filesizeformat
from django.utils.dateparse import parse_datetime
from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    id = serializers.CharField()
    short_id = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    created = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    def get_size(self, obj):
        return filesizeformat(obj.attrs['Size'])

    def get_created(self, obj):
        date_time = parse_datetime(obj.attrs['Created'])
        return serializers.DateTimeField().to_representation(date_time)


class ContainerSerializer(serializers.Serializer):
    short_id = serializers.CharField()
    id = serializers.CharField()
    name = serializers.CharField()
    status = serializers.CharField()
    # created = serializers.DateTimeField(source='attrs.Created')
    cmd = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    ip_address = serializers.CharField(source='attrs.NetworkSettings.IPAddress')
    image = ImageSerializer()

    def get_created(self, obj):
        date_time = parse_datetime(obj.attrs['Created'])
        return serializers.DateTimeField().to_representation(date_time)

    def get_cmd(self, obj):
        entry_point = obj.attrs['Config']['Entrypoint'] or []
        cmd = obj.attrs['Config']['Cmd'] or []
        entry_point.extend(cmd)
        return ' '.join(entry_point)


class Docker:
    def __init__(self, url, *args, **kwargs):
        self.client = docker.DockerClient(base_url=url, version='auto', timeout=10)

    def ping(self):
        try:
            self.client.ping()
        except docker.error.APIError:
            return False
        else:
            return True

    def container_list(self):
        obj_list = self.client.containers.list(all=True)
        return ContainerSerializer(obj_list, many=True).data
