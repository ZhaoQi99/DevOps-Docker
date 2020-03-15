from rest_framework import serializers

from utils.serializer import IdSerializer

from .models import Host


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'
        read_only_fields = ('id', )


class CreateHostSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    port = serializers.IntegerField(required=True, max_value=65535, min_value=1)

    class Meta:
        model = Host
        fields = '__all__'


class UpdateHostSerializer(HostSerializer, IdSerializer):
    port = serializers.IntegerField(required=True, max_value=65535, min_value=1)
