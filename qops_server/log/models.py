from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import Permission, User


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    permission = models.ForeignKey(Permission, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(_('create time'), auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    data = JSONField(verbose_name=_('request data'), blank=True, null=True, default=dict)

    class Meta:
        db_table = 'logs'
        verbose_name = _('log')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip
