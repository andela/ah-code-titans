from authors.base_test_config import TestConfiguration
from django.urls import reverse
from rest_framework import status


class TestGeneralRoutes(TestConfiguration):
    """
    test suite for getting all general routes
    """

    def test_get_home_page(self):

        response = self.client.get(reverse("home"))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_privacy_page(self):

        response = self.client.get(reverse("privacy"))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
