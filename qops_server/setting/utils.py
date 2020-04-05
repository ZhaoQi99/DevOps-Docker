from functools import lru_cache

from django.utils.translation import gettext_lazy as _

from utils.exceptions import SettingNotSet

from .models import Setting


class AppSetting:
    @classmethod
    @lru_cache(maxsize=64)
    def get(cls, key):
        info = Setting.objects.filter(key=key).first()
        if not info:
            raise SettingNotSet(_(f'Setting {key} has not set.'))
        return info.value

    @classmethod
    def get_default(cls, key, default=None):
        info = Setting.objects.filter(key=key).first()
        if not info:
            return default
        return info.value

    @classmethod
    def set(cls, key, value, desc=None):
        Setting.objects.update_or_create(key=key, defaults={'value': value, 'desc': desc})
