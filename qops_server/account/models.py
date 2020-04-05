import binascii
import os

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def update_last_login(sender, user, **kwargs):
    """
    A signal receiver which updates the last_login date for
    the user logging in.
    """
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])


class UserManage(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    USERNAME_FIELD = 'username'
    USER_TYPE = [('local', 'local'), ('ldap', 'ldap')]
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_admin = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    roles = models.ManyToManyField('Role', verbose_name=_('user roles'), blank=True)
    nick_name = models.CharField(_('nick name'), max_length=50, blank=False, null=True)
    type = models.CharField(_('user type'), choices=USER_TYPE, max_length=20, default='local', null=False)
    objects = UserManage()

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def authenticate(self, password):
        return self.check_password(password)

    class Meta:
        ordering = ['username']
        verbose_name = _('user')
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.username}'


def _default_expire_time():
    return timezone.now() + Token.token_expire


class Token(models.Model):
    token_length = settings.AUTH_CONFIG.get('TOKEN_LENGTH')
    token_expire = settings.AUTH_CONFIG.get('AUTH_TOKEN_EXPIRE')
    user = models.ForeignKey(
        'User', verbose_name=_("User"), related_name='tokens', on_delete=models.CASCADE, null=True, blank=False
    )
    created = models.DateTimeField(_('create time'), auto_now_add=True)
    expired = models.DateTimeField(_('token expire time'), default=_default_expire_time)
    token = models.TextField(_('token'), blank=True)

    class Meta:
        ordering = ('-created', )
        verbose_name = _("token")
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Token for {self.user.username} ({self.token})'

    def generate_key(self):
        return binascii.hexlify(os.urandom(int(self.token_length / 2))).decode()

    def verify(self):
        return self.check_exp() and self.token_length == len(self.token)

    def check_exp(self):
        return timezone.now() < self.expired

    def refresh_token(self):
        self.token = self.generate_key()
        self.expired = timezone.now() + self.token_expire
        self.save(update_fields=['token', 'expired'])

    def refresf_exp(self):
        self.expired = timezone.now() + self.token_expire
        self.save(update_fields=['expired'])

    @classmethod
    def create_token(cls, user):
        return Token.objects.create(user=user).token


class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')
    permissions = models.ManyToManyField('Permission', verbose_name=_('role permissions'), blank=True)
    menus = models.ManyToManyField('Menu', verbose_name=_('role menu'), blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = verbose_name


class Menu(models.Model):
    name = models.CharField(max_length=50, blank=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, blank=False)

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Permission(models.Model):
    METHOD_CHOICES = (('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('ALL', 'ALL'))
    url = models.CharField(max_length=50, verbose_name=_('url'))
    name = models.CharField(max_length=50, verbose_name=_('name'))
    method = models.CharField(max_length=10, verbose_name=_('HTTP method'), choices=METHOD_CHOICES, default='ALL')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
