# module import
from django.urls import reverse
from rest_framework import status

# local import
from authors.base_test_config import TestConfiguration


class TestLogin(TestConfiguration):
    def login(self, data):
        """ function used to login a user """
        return self.client.post(
            reverse("user_login"),
            data,
            content_type='application/json'
        )

    def test_incorrect_password(self):
        """ test incorrect password login """
        self.user["user"]["password"] = "kims"
        response = self.login(self.user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_login_email_does_not_exist(self):
        """ test login user does not exist """
        self.user["user"]["email"] = "kimame@gmail.com"
        response = self.login(self.user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_login_with_empty_email_field(self):
        """ test login with empty fields """

        self.user["user"]["email"] = ""
        response = self.login(self.user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data["errors"]["email"][0],
            "This field may not be blank.")

    def test_login_with_empty_password_field(self):
        """ test login with empty fields """
        self.user["user"]["password"] = ""
        response = self.login(self.user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data["errors"]["password"][0],
            "This field may not be blank."
        )

    def test_login_with_inactive_account(self):
        """Test login with an inactive account"""
        response = self.login(self.user)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
        self.assertIn(
            response.data['errors']['error'][0],
            "A user with this email and password was not found."
        )
