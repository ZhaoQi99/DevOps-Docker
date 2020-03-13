from rest_framework import serializers

from utils.serializer import IdSerializer

from .models import Menu, Permission, Role, User


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


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', )


class UpdateUserSerializer(serializers.ModelSerializer, IdSerializer):
    class Meta:
        model = User
        exclude = ('password', 'username')
        read_only_fields = ('id', )


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ('id', )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordSerializer(IdSerializer):
    password = serializers.CharField(required=True)
