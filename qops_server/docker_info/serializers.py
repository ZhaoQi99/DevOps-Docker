from rest_framework import serializers


class ListDockerInfoSerializer(serializers.Serializer):
    host_id = serializers.IntegerField(required=True)
    refresh = serializers.BooleanField(default=False)
