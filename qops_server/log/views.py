from utils.api import APIView

from .models import Log
from .serializers import LogSerializer


class LogView(APIView):
    def get(self, request):
        queryset = Log.objects.all()
        return self.success(self.paginate_data(request, queryset, LogSerializer))
