from django.utils.translation import gettext_lazy as _

from account.models import Token, User
from utils.api import APIView
from utils.exceptions import AuthenticationFailed, UserIsNotActive, UsertDoesNotExist

from .serializers import LoginSerializer
from .signals import user_logged_in


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
