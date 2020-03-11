from utils.api import APIView

from ..models import Permission
from ..serializers import PermissionSerializer


class PermissionListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Permission.objects.all()
        return self.success(self.paginate_data(request, queryset, PermissionSerializer))
