from authors.base_test_config import TestUsingLoggedInUser
from .test_config import TestConfig
from django.urls import reverse
from rest_framework import status
from authors.response import RESPONSE


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

    def test_create_article_with_invalid_tag_list(self):
        """
        test invalid tag field
        """
        response = self.create_article(self.article_data_invalid_tag_field)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["tag_list"][0],
                         RESPONSE["invalid_field"].format("tag_list"))

    def test_create_article_with_invalid_tag(self):
        """
        test invalid tag
        """
        response = self.create_article(self.article_data_invalid_tag)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["tag_list"][0],
                         RESPONSE["invalid_field"].format("tag"))

    def test_create_article_with_empty_taglist(self):
        """
        test user can create an article with an empty tag field
        """
        response = self.create_article(self.article_data_2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
