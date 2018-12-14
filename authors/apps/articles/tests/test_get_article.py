from authors.base_test_config import TestConfiguration
from .test_config import TestConfig
from django.urls import reverse
from rest_framework import status


class TestArticles(TestConfiguration, TestConfig):
    """
    test suite for getting articles
    """

    def test_get_all_articles(self):
        """
        test get all articles
        """

        response = self.client.get(
            reverse("all_articles"),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

