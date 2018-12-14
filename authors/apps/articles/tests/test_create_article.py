from authors.base_test_config import TestUsingLoggedInUser
from .test_config import TestConfig
from django.urls import reverse
from rest_framework import status


class TestArticles(TestUsingLoggedInUser, TestConfig):
    """
    test suite for creation for articles
    """

    def create_article(self, data):

        response = self.client.post(
            reverse("articles"),
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token {}'.format(self.access_token)
        )

        return response

    def test_create_article(self):
        """
        test create an article
        """
        response = self.create_article(self.article_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_article_with_invalid_title(self):
        """
        test create article with invalid title
        """

    def test_unauthorized_post_article(self):
        """
        test unauthorized posting of an article
        """
        response = self.client.post(
            reverse("articles"),
            self.article_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
