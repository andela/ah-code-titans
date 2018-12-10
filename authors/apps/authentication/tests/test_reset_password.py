# module import
from django.urls import reverse
from rest_framework import status

# local import
from authors.base_test_config import TestConfiguration

test_token = None


class TestResetPassword(TestConfiguration):
    """ Test mock data """
    user_email = [
        {
            "user": {
                "password": ""
            }
        },
        {
            "user": {
                "password": "Mase"
            }
        },
        {
            "user": {
                "password": "Masesey"
            }
        },
        {
            "user": {
                "password": "Masesey@1"
            }
        }
    ]

    def submit_email(self, data):
        return self.client.post(
            reverse("reset_request"),
            data,
            content_type='application/json')

    def edit_password(self, data):
        return self.client.put(
            test_token,
            data,
            content_type='application/json')

    def test_generate_reset_link(self):
        response = self.submit_email(self.registered_user_email)
        global test_token
        test_token = response.json()['user'].get('linker')

    def test_user_enter_empty_field(self):
        response = self.edit_password(self.user_email[0])

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json(),
            {"errors": [
                "Password should have at least one number, an uppercase or lowercase letter or one special character."
            ]
            })

    def test_user_enter_short_password(self):
        response = self.edit_password(self.user_email[1])

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json(),
            {"errors": [
                "Password should have at least one number, an uppercase or lowercase letter or one special character."
            ]
            })

    def test_user_enter_weak_password(self):
        response = self.edit_password(self.user_email[2])

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json(),
            {"errors": [
                "Password should have at least one number, an uppercase or lowercase letter or one special character."
            ]
            })

    def test_user_enter_correct_password(self):
        response = self.edit_password(self.user_email[3])

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {'user': {'message': 'Your password was successfully changed'}})
