from django.urls import reverse
from rest_framework import status
from authors.base_test_config import TestUsingLoggedInUser
from authors.apps.articles.tests.test_config import TestConfig


class TestReadArticle(TestUsingLoggedInUser, TestConfig):
    """
    test suite for user read stat
    """

    def retrieve_user_read_stats(self):
        return self.client.get(
            reverse("user_read_stats"),
            content_type='application/json',
            HTTP_AUTHORIZATION="Token {}".format(self.access_token)
        )

    def test_1_start_read_article(self):
        """
        test add article as viewed and read false
        """
        response = self.get_request("article")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2 = self.retrieve_user_read_stats()
        self.check_if_article_is_read(response2, False)

        response = self.get_request("article_read")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2 = self.retrieve_user_read_stats()
        self.check_if_article_is_read(response2, True)

    def test_update_a_non_existing_article_status__to_read(self):

        response = self.get_request("article")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2 = self.retrieve_user_read_stats()
        self.check_if_article_is_read(response2, False)

        update_to_read = self.client.get(
            reverse(
                "article_read",
                kwargs={
                    "slug": "self.stored_articles[2].slug"
                }),
            content_type='application/json',
            HTTP_AUTHORIZATION="Token {}".format(self.access_token)
        )
        self.assertEqual(update_to_read.status_code, status.HTTP_404_NOT_FOUND)

    def get_request(self, url):
        return self.client.get(
            reverse(
                url,
                kwargs={
                    "slug": self.stored_articles[2].slug
                }),
            content_type='application/json',
            HTTP_AUTHORIZATION="Token {}".format(self.access_token)
        )

    def check_if_article_is_read(self, response, is_read):
        read_article = None

        for article in response.data['results']:
            if article['article']['slug'] == self.stored_articles[2].slug:
                read_article = article
                break

        self.assertNotEqual(read_article, None)
        self.assertEqual(read_article['read'], is_read)
