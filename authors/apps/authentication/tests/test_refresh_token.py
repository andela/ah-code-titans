from rest_framework import status
from django.urls import reverse

from authors.base_test_config import TestUsingLoggedInUser
from authors.response import RESPONSE


class TestPostNewArticleComment(TestUsingLoggedInUser):

    def setUp(self):
        super().setUp()

    def get_access_token(self, token):
        return self.client.get(
            reverse("token_refresh"),
            content_type='application/json',
            HTTP_AUTHORIZATION="Token {}".format(token)
        )

    def test_using_access_token(self):
        response = self.get_access_token(self.access_token)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(
            response.data['message'],
            RESPONSE['token']['refresh']['invalid']
        )

    def test_using_valid_refresh_token(self):
        response = self.get_access_token(self.refresh_token)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['message'],
            RESPONSE['token']['refresh']['valid']
        )

        self.assertIn(
            'access_token',
            response.data,
        )

        self.assertNotEqual(
            response.data['access_token'],
            ""
        )
