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
        self.assertIn(
            "password with at least 8 characters",
            response.data["errors"]["password"][0]
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

    def test_uppercase_password(self):
        """ test that the password contains an uppercase letter """
        self.new_user["user"]["password"] = 'codetitans32'
        response = self.register_user(self.new_user)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            "at least one number, an uppercase or lowercase letter",
            response.data["errors"]["password"][0]
        )

    def test_lowercase_password(self):
        """ test that the password contains an lowercase letter """
        self.new_user["user"]["password"] = 'CODETITANS32'

        response = self.register_user(self.new_user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            "at least one number, an uppercase or lowercase letter",
            response.data["errors"]["password"][0]
        )

    def test_special_character_password(self):
        """ test that the password contains a special character """
        self.new_user["user"]["password"] = 'Codetitans32'
        response = self.register_user(self.new_user)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            "lowercase letter or one special character",
            response.data["errors"]["password"][0]
        )

    def test_number_in_password(self):
        """ test that the password contains a number """
        self.new_user["user"]["password"] = 'Codetitans@!'
        response = self.register_user(self.new_user)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            "Password should have at least one number",
            response.data["errors"]["password"][0]
        )

    def test_register_user(self):
        """ test register user """
        response = self.register_user(self.new_user)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertIn(
            'token',
            response.data,
            "Response body does not contain access token!"
        )

    def test_existing_email(self):
        """ test register with existing user email """
        self.new_user["user"]["email"] = self.user["user"]["email"]

        response = self.register_user(self.new_user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_existing_username(self):
        """ test register with existing username """
        self.new_user["user"]["username"] = self.user["user"]["username"]
        response = self.register_user(self.new_user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
