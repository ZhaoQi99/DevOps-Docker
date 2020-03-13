from utils.api import APIView

from ..models import Role
from ..serializers import RoleSerializer


class RoleView(APIView):
    def get(self, request):
        queryset = Role.objects.all()
        return self.success(self.paginate_data(request, queryset, RoleSerializer))
