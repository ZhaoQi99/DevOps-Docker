from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from account.models import Menu, Token, User
from utils.api import APIView
from utils.exceptions import AuthenticationFailed, UserIsNotActive, UsertDoesNotExist

from ..serializers import LoginSerializer
from ..signals import user_logged_in


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(errors=serializer.errors)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = User.objects.filter(username=username).first()
        if not user:
            raise UsertDoesNotExist
        if not user.is_active:
            raise UserIsNotActive
        if not user.authenticate(password):
            raise AuthenticationFailed(_('Password is incorrect.'))
        token = Token.create_token(user)
        user_logged_in.send(sender=user.__class__, user=user)
        data = {'token': token}
        return self.success(data)


class SelfView(APIView):
    def get(self, request):
        roles = request.user.roles.all()
        user_menus = set()
        for role in roles:
            user_menus.update(list(role.menus.all().values_list("key", flat=True)))
        menus = dict()
        for key in list(Menu.objects.all().values_list('key', flat=True)):
            menus[key] = True if key in user_menus else False
        return self.success({'menus': menus})
