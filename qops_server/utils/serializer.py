from rest_framework import serializers


class IdSerializer(serializers.Serializer):
    obj_id = serializers.IntegerField(required=True)
