from rest_framework import serializers


class SettingSerilizer(serializers.Serializer):
    key = serializers.CharField()
