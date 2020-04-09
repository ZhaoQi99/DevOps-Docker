import json
import traceback

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from account.models import Permission, Token
from log.models import Log
from utils.exceptions import AuthenticationFailed, BaseException, NotAuthenticated, UnknownException


class MyAuthentication:
    def authenticate(self, request):
        header = self.authenticate_header(request)
        raw_token = self.get_raw_token(header)
        token_obj = Token.objects.filter(token=raw_token).first()
        if not (token_obj and token_obj.verify()):
            raise AuthenticationFailed
        if token_obj.expired - timezone.now() < Token.token_expire:  # token快要过期了
            token_obj.refresf_exp()
        return token_obj.user, token_obj.token

    def get_raw_token(self, header):
        return header.split()[1]

    def authenticate_header(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        if header is None:
            raise NotAuthenticated
        parts = header.split()
        if len(parts) == 0 or len(parts) != 2:
            raise NotAuthenticated
        return header


class MyMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if any(request.path.startswith(x) for x in settings.AUTH_CONFIG['AUTH_EXCLUDE']):
            return None
        if request.path.startswith('/api/hosts/ssh/'):  # auth check in view
            return None
        try:
            # Auth
            user, token = MyAuthentication().authenticate(request)
            request.user = user
            request.token = token
        except Exception as e:
            if not isinstance(e, BaseException):
                e = UnknownException(msg=str(e))
            return JsonResponse(e.as_dict(), status=e.get_http_code())
        return None


class ProcessExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG is True:
            print(request.body)
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if settings.DEBUG is True:
            try:
                print(request.data)
            except Exception:
                pass
            traceback.print_exc()
            # return None  # using default debug page
        if not isinstance(exception, BaseException):
            exception = UnknownException(msg=str(exception), errors=traceback.format_exc().splitlines())
        return JsonResponse(exception.as_dict(), status=exception.get_http_code())


class PermissionMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/admin'):
            return None
        path = request.path
        method = request.method

        permission = Permission.objects.filter(url=path, method=method).first()
        request.permission = permission
        if not permission:
            return None
        # Todo: validate permission


class LogMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/admin'):
            return None
        user = getattr(request, 'user', None)
        permission = getattr(request, 'permission', None)

        data = json.loads(request.body) if request.body else {}
        ip = request.META['REMOTE_ADDR']
        # ip = request.META['HTTP_X_FORWARDED_FOR']
        if permission:
            Log.objects.create(user=user, permission=permission, ip=ip, data=data)
