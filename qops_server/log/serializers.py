from rest_framework import serializers

from account.serializers import PermissionSerializer, UserListSerializer

from .models import Log


class LogSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    permission = PermissionSerializer()

    class Meta:
        model = Log
        fields = '__all__'
