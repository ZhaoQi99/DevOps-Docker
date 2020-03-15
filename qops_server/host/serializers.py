from rest_framework import serializers

from utils.serializer import IdSerializer

from .models import Host


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'
        read_only_fields = ('id', )


class UpdateHostSerializer(HostSerializer, IdSerializer):
    pass
