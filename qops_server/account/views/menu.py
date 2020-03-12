from utils.api import APIView
from utils.exceptions import MenuDoesNotExist
from utils.serializer import IdSerializer

from ..models import Menu
from ..serializers import MenuSerializer, UpdateMenuSerializer


class MenuView(APIView):
    def get(self, request):
        queryset = Menu.objects.all()
        return self.success(self.paginate_data(request, queryset, MenuSerializer))

    def delete(self, request, *args, **kwargs):
        serializer = IdSerializer(data=request.data)

        if not serializer.is_valid():
            self.error(serializer.errors)
        obj_id = serializer.validated_data['obj_id']
        Menu.objects.filter(pk=obj_id).delete()
        return self.success(status=204)

    def put(self, request, *args, **kwargs):
        serializer = UpdateMenuSerializer(data=request.data)

        if not serializer.is_valid():
            self.error(serializer.errors)
        obj_id = serializer.validated_data['obj_id']
        queryset = Menu.objects.filter(pk=obj_id)
        if not queryset:
            raise MenuDoesNotExist
        serializer.validated_data.pop('obj_id')
        queryset.update(**serializer.validated_data)
        obj = queryset.first()
        return self.success(MenuSerializer(obj).data)

    def post(self, request, *args, **kwargs):
        serializer = MenuSerializer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        Menu.objects.create(**serializer.validated_data)
        return self.success(status=201)
