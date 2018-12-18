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
        article_count = response.data['count']
        paginated_articles = len(response.data['results'])
        next_page_url = response.data['next']
        query_params = next_page_url.split('?')[-1]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(query_params, 'limit=10&offset=10')
        self.assertEqual(article_count, 50)
        self.assertEqual(paginated_articles, 10)

