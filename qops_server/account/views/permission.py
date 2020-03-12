from utils.api import APIView
from utils.exceptions import PermissionDoesNotExist
from utils.serializer import IdSerializer

from ..models import Permission
from ..serializers import PermissionSerializer, UpdatePermissionSerializer


class PermissionListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Permission.objects.all()
        return self.success(self.paginate_data(request, queryset, PermissionSerializer))

    def delete(self, request, *args, **kwargs):
        serializer = IdSerializer(data=request.data)

        if not serializer.is_valid():
            self.error(serializer.errors)
        obj_id = serializer.validated_data['obj_id']
        Permission.objects.filter(pk=obj_id).delete()
        return self.success(status=204)

    def put(self, request, *args, **kwargs):
        serializer = UpdatePermissionSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        obj_id = serializer.validated_data['obj_id']
        queryset = Permission.objects.filter(pk=obj_id)
        if not queryset:
            raise PermissionDoesNotExist
        serializer.validated_data.pop('obj_id')
        queryset.update(**serializer.validated_data)
        obj = queryset.first()
        return self.success(PermissionSerializer(obj).data)

    def post(self, request, *args, **kwargs):
        serializer = PermissionSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        Permission.objects.create(**serializer.validated_data)
        return self.success(status=201)
