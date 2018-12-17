from authors.base_test_config import TestUsingLoggedInUser
from django.urls import reverse
from rest_framework import status

from authors.response import RESPONSE


class TestArticleShare(TestUsingLoggedInUser):
    """
    Test suite for getting article share links
    """

    def get_share_link(self, slug, provider):
        return self.client.get(
            reverse(
                "share_article",
                kwargs={
                    "slug": slug,
                    "provider": provider
                }),
            HTTP_AUTHORIZATION="Token {}".format(self.access_token)
        )

    def get_using_valid_provider(self, provider):
        response = self.get_share_link(self.stored_articles[0].slug, provider)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['share']['link'], "")
        self.assertEqual(response.data['share']['provider'], provider)

    def test_get_facebook_link(self):
        """
        This tests the retrieval of the facebook share link
        """
        self.get_using_valid_provider("facebook")

    def test_get_twitter_link(self):
        """
        This tests the retrieval of the twitter share link
        """
        self.get_using_valid_provider("twitter")

    def test_get_reddit_link(self):
        """
        This tests the retrieval of the reddit share link
        """
        self.get_using_valid_provider("reddit")

    def test_get_linkedin_link(self):
        """
        This tests the retrieval of the linkedin share link
        """
        self.get_using_valid_provider("linkedin")

    def test_get_email_link(self):
        """
        This tests the retrieval of the email share link
        """
        self.get_using_valid_provider("email")

    def test_using_unexisting_article_slug(self):
        """
        This tests the endpoint using an unexisting article's slug. An error is expected
        be sent back.
        """
        response = self.get_share_link("this-article-does-not-exist", "facebook")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['errors']['article'],
            RESPONSE['not_found'].format(data="Article")
        )

    def test_using_invalid_provider(self):
        """
        This tests the endpoint using an unexisting article's slug. An error is expected
        be sent back.
        """
        response = self.get_share_link(
            self.stored_articles[0].slug,
            "facebook1"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['errors']['provider'],
            RESPONSE['invalid_field'].format("provider")
        )
