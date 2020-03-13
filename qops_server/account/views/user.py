from django.db import transaction
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from account.models import Menu, Token, User
from utils.api import APIView
from utils.exceptions import AuthenticationFailed, OldPasswordIncorrect, UserIsNotActive, UsertDoesNotExist
from utils.serializer import IdSerializer

from ..serializers import (
    ChangePasswordSerializer, LoginSerializer, ResetPasswordSerializer, UpdateUserSerializer, UserListSerializer,
    UserSerializer
)
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
        data = {'token': token, 'nick_name': user.nick_name, 'user_id': user.id}
        return self.success(data)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        user = request.user
        if not user.authenticate(old_password):
            raise OldPasswordIncorrect
        user.set_password(new_password)
        user.save(update_fields=['password'])
        return self.success(status=201)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        password = serializer.validated_data['password']
        obj_id = serializer.validated_data['obj_id']
        user = User.objects.filter(pk=obj_id).first()
        if not user:
            raise UsertDoesNotExist
        user.set_password(password)
        user.save(update_fields=['password'])
        return self.success(status=201)


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


class UserView(APIView):
    def get(self, request):
        queryset = User.objects.all()
        return self.success(self.paginate_data(request, queryset, UserListSerializer))

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        with transaction.atomic():
            roles = serializer.validated_data.pop('roles')
            user = User(**serializer.validated_data)
            user.set_password(serializer.validated_data['password'])
            user.save()
            user.roles.set(roles)
        return self.success(status=201)

    def put(self, request):
        serializer = UpdateUserSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        with transaction.atomic():
            roles = serializer.validated_data.pop('roles')
            user_id = serializer.validated_data.pop('obj_id')
            queryset = User.objects.filter(pk=user_id)
            if not queryset:
                raise UsertDoesNotExist
            queryset.update(**serializer.validated_data)
            user = queryset.first()
            user.roles.set(roles)
        return self.success(status=201)

    def delete(self, request):
        serializer = IdSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        obj_id = serializer.validated_data['obj_id']
        queryset = User.objects.filter(pk=obj_id)
        if not queryset:
            raise UsertDoesNotExist
        queryset.delete()
        return self.success(status=204)
