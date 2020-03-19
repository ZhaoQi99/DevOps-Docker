from utils.api import APIView
from utils.exceptions import SettingNotSet

from .serializers import SettingSerilizer
from .utils import AppSetting


class SettingView(APIView):
    def post(self, request):
        serializer = SettingSerilizer(data=request.data)
        if not serializer.is_valid():
            self.error(serializer.errors)
        key = serializer.validated_data['key']
        value = AppSetting.get_default(key)
        if not value:
            raise SettingNotSet
        return self.success(value)
