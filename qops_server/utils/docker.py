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
    labels = serializers.DictField()

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


class VolumeSerializer(serializers.Serializer):
    created = serializers.SerializerMethodField()
    mount_point = serializers.CharField(source='attrs.Mountpoint')
    driver = serializers.CharField(source='attrs.Driver')
    name = serializers.CharField()
    short_id = serializers.CharField()

    def get_created(self, obj):
        date_time = parse_datetime(obj.attrs['CreatedAt'])
        return serializers.DateTimeField().to_representation(date_time)


class NetworkSerializer(serializers.Serializer):
    name = serializers.CharField()
    scope = serializers.CharField(source='attrs.Scope')
    driver = serializers.CharField(source='attrs.Driver')
    attachable = serializers.BooleanField(source='attrs.Attachable')
    internal = serializers.BooleanField(source='attrs.Internal')
    ipam_driver = serializers.CharField(source='attrs.IPAM.Driver')
    ipam_subnet = serializers.SerializerMethodField()
    ipam_gateway = serializers.SerializerMethodField()

    def get_ipam_subnet(self, obj):
        config = obj.attrs['IPAM']['Config']
        return [_['Subnet'] for _ in config]

    def get_ipam_gateway(self, obj):
        config = obj.attrs['IPAM']['Config']
        return [_['Gateway'] for _ in config]


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

    def image_list(self):
        obj_list = self.client.images.list()
        return ImageSerializer(obj_list, many=True).data

    def volume_list(self):
        obj_list = self.client.volumes.list()
        return VolumeSerializer(obj_list, many=True).data

    def network_list(self):
        obj_list = self.client.networks.list()
        return NetworkSerializer(obj_list, many=True).data
