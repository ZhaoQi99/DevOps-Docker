from abc import ABCMeta

from django.utils.translation import gettext_lazy as _


class BaseException(Exception):
    metaclass = ABCMeta

    def __init__(self, msg=None, errors=None):
        if msg:
            self.msg = msg
        self.errors = errors if errors else list()

    def __str__(self):
        return str(self.msg)

    @classmethod
    def get_http_code(self):
        return getattr(self, 'http_code', 200)

    def as_dict(self):
        ret = {'msg': getattr(self, 'msg', ''), 'status': getattr(self, 'status', ''), 'errors': self.errors}
        return ret


# success
# {'status': 0, 'data': ''}
# fail
# {'status': 1000, 'msg': '',errors:[]}


class UnknownException(BaseException):
    http_code = 500
    status = 1000
    msg = _('Unknown exception.')


class AuthenticationFailed(BaseException):
    http_code = 401
    status = 1001
    msg = _('Token is invalid or expired.')


class NotAuthenticated(BaseException):
    http_code = 401
    status = 1002
    msg = _('Authentication token were not provided.')


class ObjectDoesNotExist(BaseException):
    status = 1003
    msg = _("Object does not exists.")


class ValidationError(BaseException):
    http_code = 400
    status = 1004
    msg = _('Parameter invalid.')


class UsertDoesNotExist(ObjectDoesNotExist):
    msg = _('User does not exists.')


class UserIsNotActive(BaseException):
    status = 1005
    msg = _('User is not active.')


class PermissionDoesNotExist(ObjectDoesNotExist):
    msg = _('Permission does not exists.')


class MenuDoesNotExist(ObjectDoesNotExist):
    msg = _('Menu does not exists.')


class OldPasswordIncorrect(BaseException):
    status = 1006
    msg = _('Old password is incorrect.')


class HostDoesNotExist(ObjectDoesNotExist):
    msg = _('Host does not exists.')


class SshConnectFailed(BaseException):
    status = 1007
    msg = _('SSH connect failed.')


# _('The two password fields didn\'t match.')
# class PasswordIncorrect(ObjectDoesNotExist):
#     status = 1004
#     msg = ErrorMsg.PASSWORD_INCORRECT

# class RoleDoesNoeExist(ObjectDoesNotExist):
#     msg = ErrorMsg.ROLE_DOES_NOE_EXIST
