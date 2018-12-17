from django.urls import reverse
from rest_framework import status
from authors.base_test_config import TestUsingLoggedInUser
from .test_config import TestConfig


class RetrieveSpecificArticle(TestUsingLoggedInUser, TestConfig):
    """
    Test suite for retrieving specific articles
    """

    def retrieve_article(self, slug):
        return self.client.get(
            reverse(
                "article",
                kwargs={
                    "slug": slug
                }),
            content_type='application/json')

    def test_get_specific_article(self):
        """
        Test to retrieve a specific article
        """
        self.client.post(
            reverse("articles"),
            self.article_data,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token {}'.format(self.access_token)
        )
        response = self.retrieve_article(
            "javascript-es6"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['tag_list'], [])

    def test_get_uncreated_article(self):
        """
        Test on trying to retrieve a no existing article
        """
        response = self.retrieve_article(
            self.stored_articles[0].slug + 'oo'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
