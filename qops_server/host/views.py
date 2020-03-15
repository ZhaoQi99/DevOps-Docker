from django.shortcuts import render

from account.models import Token
from utils.api import APIView
from utils.exceptions import AuthenticationFailed, HostDoesNotExist
from utils.serializer import IdSerializer

from .models import Host
from .serializers import HostSerializer, UpdateHostSerializer


class HostView(APIView):
    def get(self, request):
        queryset = Host.objects.all()
        hosts = HostSerializer(queryset, many=True).data
        categorys = queryset.values_list("category", flat=True).distinct()
        categorys = list(set(categorys))
        return self.success({'hosts': hosts, 'categorys': categorys})

    def post(self, request):
        serializer = HostSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
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
