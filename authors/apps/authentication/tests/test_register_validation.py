from rest_framework import status
from django.urls import reverse

# local import
from .test_config import TestConfiguration


class TestRegister(TestConfiguration):
    """ Test suite for user registration """

    def register_user(self, data):
        """ function register a new user """
        return self.client.post(
            reverse("create_user"),
            data,
            content_type='application/json'
        )

    def test_username_length(self):
            """ test if username is at least 4 characters """
            self.new_user["user"]["username"] = 'co2'

            response = self.register_user(self.new_user)
            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST
            )

            self.assertIn(
                "Username should be at least 4 characters long",
                response.data["errors"]["username"][0]
            )

    def test_invalid_username(self):
            """ test if username contains numbers only """
            self.new_user["user"]["username"] = 'co2'

            response = self.register_user(self.new_user)
            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST
            )

            self.assertIn(
                "and should not contain numbers only",
                response.data["errors"]["username"][0]
            )

