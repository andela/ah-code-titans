# module import
from django.urls import reverse
from rest_framework import status

# local import
from .test_config import TestConfiguration


class TestReset(TestConfiguration):
    """Testing mock data"""
    user_email = [
        {
            "user": {
                "email": ""
            }
        },
        {
            "user": {
                "email": "dariosmasaysay.com"
            }
        },
        {
            "user": {
                "email": "darios@masaysay"
            }
        }
    ]

    def submit_email(self, data):
        return self.client.post(
            reverse("reset_request"),
            data,
            content_type='application/json')

    def test_user_request_reset_link_empty_email(self):
        response = self.submit_email(self.user_email[0])

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json(),
            {'errors': {'email': ['This field may not be blank.']}})

    def test_user_enter_email_no_at(self):
        response = self.submit_email(self.user_email[1])

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json(),
            {'errors': {'email': ['Enter a valid email address.']}})

    def test_user_enter_email_no_ending(self):
        response = self.submit_email(self.user_email[2])

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json(),
            {'errors': {'email': ['Enter a valid email address.']}})

    def test_user_enter_correct_mail(self):
        response = self.submit_email(self.registered_user_email)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK)

        self.assertEqual(
            response.json()['user']['message'],
            "Check your email for the link")
