from authors.base_test_config import TestUsingLoggedInUser
from .test_config import TestConfig
from django.urls import reverse
from rest_framework import status


class TestArticles(TestUsingLoggedInUser, TestConfig):
    """
    test suite for updating for articles
    """

    def update_article(self, data, slug):
        return self.client.put(
            reverse(
                "article",
                kwargs={
                    "slug": slug
                }),
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token {}'.format(self.access_token)
        )

    def test_update_an_article(self):
        """
        test update article
        """

        response = self.update_article(
            self.update_article_data,
            self.stored_articles[0].slug
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["article"]
                         ["tag_list"], self.update_article_data["article"]["tag_list"])

    def test_update_article_without_taglist_field(self):
        """
        test update article without taglist field
        """
        response = self.update_article(
            self.article_data_no_taglist,
            self.stored_articles[0].slug
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_non_existing_article(self):
        """
        test delete a non existing article
        """
        response = self.update_article(
            self.article_data_2,
            "this-is-a-non-existing-slug"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_update_article(self):
        """
        test unauthorized updating of an article
        """
        response = self.client.put(
            reverse(
                "article",
                kwargs={
                    "slug": self.stored_articles[0].slug
                }),
            self.article_data,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
