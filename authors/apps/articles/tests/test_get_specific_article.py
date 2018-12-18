from django.urls import reverse

from rest_framework import status

from authors.base_test_config import TestConfiguration


class RetrieveSpecificArticle(TestConfiguration):
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
        response = self.retrieve_article(
            self.stored_articles[0].slug
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_uncreated_article(self):
        """
        Test on trying to retrieve a no existing article
        """
        response = self.retrieve_article(
            self.stored_articles[0].slug + 'oo'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
