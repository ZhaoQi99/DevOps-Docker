from utils.api import APITestCase, ContentType

from .models import User


class LoginViewTestCase(APITestCase):
    def setUp(self):
        self.url = self.reverse('user_login')

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test1', password='test1')
        User.objects.create_user(username='test2', password='test2', is_active=False)

    def test_login_fail(self):
        res = self.client.post(
            self.url,
            data={
                "username": "john",
                "password": "smith",
                "type": "local"
            },
            content_type=ContentType.JSON_REQUEST
        )
        self.assertEqual(res.status_code, 200)
        self.assertFailed(res, 'User does not exists.')

        res = self.client.post(
            self.url,
            data={
                "username": "test1",
                "password": "smith",
                "type": "local"
            },
            content_type=ContentType.JSON_REQUEST
        )
        self.assertEqual(res.status_code, 401)
        self.assertFailed(res, 'Password is incorrect.')

        res = self.client.post(
            self.url,
            data={
                "username": "test2",
                "password": "test2",
                "type": "local"
            },
            content_type=ContentType.JSON_REQUEST
        )
        self.assertEqual(res.status_code, 200)
        self.assertFailed(res, 'User is not active.')

    def test_login_success(self):
        res = self.client.post(
            self.url,
            data={
                "username": "test1",
                "password": "test1",
                "type": "local"
            },
            content_type=ContentType.JSON_REQUEST
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 0)
        self.assertIsInstance(res.json()['data']['token'], str)
