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

    def test_empty_username(self):
        """ test empty username """

        self.new_user["user"]["username"] = ''

        response = self.register_user(self.new_user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.data["errors"]["username"][0],
            "This field may not be blank."
        )

    def test_invalid_email(self):
        """ test invalid email """
        self.new_user["user"]["email"] = 'kimameß'

        response = self.register_user(self.new_user)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data["errors"]["email"][0],
            "Enter a valid email address."
        )

    def test_empty_email(self):
        """ test invalid email """
        self.new_user["user"]["email"] = ''

        response = self.register_user(self.new_user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data["errors"]["email"][0],
            "This field may not be blank."
        )

    def test_invalid_password(self):
        """ test invalid password """
        self.new_user["user"]["password"] = 'rtryyr'

        response = self.register_user(self.new_user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data["errors"]["password"][0],
            "Ensure this field has at least 8 characters."
        )

    def test_empty_password(self):
        """ test invalid password """
        self.new_user["user"]["password"] = ''
        response = self.register_user(self.new_user)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data["errors"]["password"][0],
            "This field may not be blank."
        )

    def test_register_user(self):
        """ test register user """

        response = self.register_user(self.new_user)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.data,
            {'email': f'{self.new_user["user"]["email"]}',
             'username': f'{self.new_user["user"]["username"]}'}
        )

    def test_existing_email(self):
        """ test register user """
        self.new_user["user"]["email"] = self.user["user"]["email"]

        response = self.register_user(self.new_user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_existing_username(self):
        """ test register user """
        self.new_user["user"]["username"] = self.user["user"]["username"]
        response = self.register_user(self.new_user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
