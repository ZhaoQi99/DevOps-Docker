from django.shortcuts import render

from account.models import Token
from setting.utils import AppSetting
from utils.api import APIView
from utils.exceptions import AuthenticationFailed, HostDoesNotExist, SshConnectFailed
from utils.serializer import IdSerializer
from utils.ssh import SSH

from .models import Host
from .serializers import CreateHostSerializer, HostSerializer, UpdateHostSerializer


class HostView(APIView):
    def get(self, request):
        queryset = Host.objects.all()
        hosts = HostSerializer(queryset, many=True).data
        categorys = queryset.values_list("category", flat=True).distinct()
        categorys = list(set(categorys))
        return self.success({'hosts': hosts, 'categorys': categorys})

    def post(self, request):
        serializer = CreateHostSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        hostname = serializer.validated_data['hostname']
        port = serializer.validated_data['port']
        username = serializer.validated_data['username']
        password = serializer.validated_data.get('password', None)
        if valid_ssh(hostname, port, username, password) is False:
            raise SshConnectFailed
        try:
            serializer.validated_data.pop('password')
        except Exception:
            pass
        Host.objects.create(**serializer.validated_data)
        return self.success(status=201)

    def put(self, request):
        serializer = UpdateHostSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        obj_id = serializer.validated_data.pop('obj_id')
        host = Host.objects.filter(pk=obj_id)
        if not host:
            raise HostDoesNotExist
        host.update(**serializer.validated_data)
        return self.success(status=201)

    def delete(self, request):
        serializer = IdSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        obj_id = serializer.validated_data['obj_id']
        Host.objects.filter(pk=obj_id).delete()
        return self.success(status=204)


def web_ssh(request, h_id):
    token = request.GET.get('x-token', None)
    token_obj = Token.objects.filter(token=token).first()
    if not (token_obj and token_obj.verify()):
        raise AuthenticationFailed
    host = Host.objects.filter(pk=h_id).first()
    if not host:
        raise HostDoesNotExist
    context = {'id': h_id, 'title': host.name, 'token': token}
    return render(request, 'web_ssh.html', context)


def valid_ssh(hostname, port, username, password):
    try:
        private_key = AppSetting.get('private_key')
        public_key = AppSetting.get('public_key')
    except KeyError:
        private_key, public_key = SSH.generate_key()
        AppSetting.set('private_key', private_key, 'ssh private key')
        AppSetting.set('public_key', public_key, 'ssh public key')
    if password:
        print(password)
        cli = SSH(hostname, port, username, password=password)
        try:
            cli.ping()
        except Exception:
            return False
        code, out = cli.exec_command(
            'mkdir -p -m 700 ~/.ssh && \
                echo %r >> ~/.ssh/authorized_keys && \
                chmod 600 ~/.ssh/authorized_keys' % public_key
        )
        if code != 0:
            raise Exception(f'add public key error: {out!r}')
    else:
        cli = SSH(hostname, port, username, private_key)

    try:
        cli.ping()
    except Exception:
        return False
    return True
