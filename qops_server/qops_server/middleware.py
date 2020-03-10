import traceback

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from account.models import Token
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
            print(request.data)
            traceback.print_exc()
            # return None  # using default debug page
        if not isinstance(exception, BaseException):
            exception = UnknownException(msg=str(exception))
        return JsonResponse(exception.as_dict(), status=exception.get_http_code())
