import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.test import TestCase
from django.urls import reverse
# from rest_framework.test import APIClient
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from .exceptions import ValidationError


class ContentType(object):
    # url_encoded_request = "application/x-www-form-urlencoded"
    # binary_response = "application/octet-stream"
    JSON_REQUEST = "application/json"
    JSON_RESPONSE = "application/json;charset=UTF-8"


class APIView(View):
    response_class = JsonResponse

    def response(self, data, status):
        ret = {'status': 0, 'data': data}
        return self.response_class(
            ret, encoder=DjangoJSONEncoder, status=status, content_type=ContentType.JSON_RESPONSE
        )

    def success(self, data=None, status=200):
        if not data:
            return HttpResponse(status=status)
        else:
            return self.response(data, status=status)

    def extract_errors(self, errors):
        return [f'{k}: {v[0]}' for k, v in errors.items()]

    def error(self, errors, msg=None):
        # msg = self.extract_errors(errors)
        if errors and isinstance(errors, str):
            errors = list(errors)
        raise ValidationError(msg=msg, errors=errors)  # middleware process

    def paginate_data(self, request, query_set, object_serializer=None):
        """
        :param request: django的request
        :param query_set: django model的query set或者其他list like objects
        :param object_serializer: 用来序列化query set, 如果为None, 则直接对query_set切片
        :return:
        """
        try:
            limit = int(request.GET.get("limit", "10"))
        except ValueError:
            limit = 0
        limit = 0 if limit < 0 else limit
        try:
            offset = int(request.GET.get("offset", "0"))
        except ValueError:
            offset = 0
        offset = 0 if offset < 0 else offset
        if object_serializer:
            query_set = query_set.order_by('-id')  # Todo: support order params
        results = query_set[offset:offset + limit] if limit else query_set[offset:]

        if object_serializer:
            count = query_set.count()
            results = object_serializer(results, many=True).data
        else:
            count = len(query_set)
        data = {"list": results, "total": count}
        return data

    def dispatch(self, request, *args, **kwargs):
        # loads data
        request.data = dict()
        if request.method not in [
            "GET",
        ] and request.body != b'':
            content_type = request.META.get("CONTENT_TYPE", None)
            if not content_type:
                raise ValueError(_('CONTENT_TYPE is required.'))
            if content_type == ContentType.JSON_REQUEST:
                request.data = json.loads(request.body.decode("utf-8"))
            else:
                raise ValueError(_('Unsupported content_type header.'))
        return super(APIView, self).dispatch(request, *args, **kwargs)


class APITestCase(TestCase):
    # client_class = APIClient

    # def assertSuccess(self, response):
    #     self.assertIn(response.status_code, [201, 200, 204])

    def assertFailed(self, response, msg=None):
        data = response.json()
        self.assertNotEqual(data['status'], 0)
        if msg:
            self.assertEqual(data["msg"], msg)

    def reverse(self, url_name, *args, **kwargs):
        return reverse(url_name, *args, **kwargs)
