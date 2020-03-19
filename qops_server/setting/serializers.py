from rest_framework import serializers
from .utils import AppSetting


class SettingSerilizer(serializers.Serializer):
    key = serializers.ChoiceField(choices=AppSetting.keys)