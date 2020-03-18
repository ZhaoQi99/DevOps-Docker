from rest_framework import serializers


class ListContainerSerializer(serializers.Serializer):
    host_id = serializers.IntegerField(required=True)
    refresh = serializers.BooleanField(default=False)


class ListHostImageSerializer(serializers.Serializer):
    host_id = serializers.IntegerField(required=True)
    refresh = serializers.BooleanField(default=False)