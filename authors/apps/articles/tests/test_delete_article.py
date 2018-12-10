from authors.base_test_config import TestUsingLoggedInUser
from .test_config import TestConfig
from django.urls import reverse
from rest_framework import status


class TestArticles(TestUsingLoggedInUser, TestConfig):
    """
    test suite for deleting for articles
    """

    def delete_article(self, slug):
        return self.client.delete(
            reverse(
                "article",
                kwargs={
                    "slug": slug
                }),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token {}'.format(self.access_token)
        )

    def test_delete_specific_article(self):
        """
        test get specific article
        """
        response = self.delete_article(self.stored_articles[3].slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_delete_article(self):
        """
        test unauthorized deletion of an article
        """
        response = self.client.delete(
            reverse("articles"),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_non_existing_article(self):
        """
        test delete a non existing article
        """
        response = self.delete_article("javascript-es7")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
