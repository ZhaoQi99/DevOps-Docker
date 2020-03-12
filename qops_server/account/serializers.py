from rest_framework import serializers

from utils.serializer import IdSerializer

from .models import Menu, Permission


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
        read_only_fields = ('id', )


class UpdatePermissionSerializer(PermissionSerializer, IdSerializer):
    pass


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = ('id', )


class UpdateMenuSerializer(MenuSerializer, IdSerializer):
    pass
