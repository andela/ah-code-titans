from rest_framework import status
from django.urls import reverse

from authors.base_test_config import TestConfiguration
from authors.response import RESPONSE


class TestGetArticleComments(TestConfiguration):

    def get_comments(self, slug, offset):
        return self.client.get(
            reverse(
                "article_comments_list",
                kwargs={
                    "slug": slug,
                    "offset": offset
                }
            )
        )

    def test_using_unexisting_article_slug(self):
        response = self.get_comments("this-article-does-not-exist", 0)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            response.data['errors']['article'],
            RESPONSE['not_found'].format(data="Article")
        )

    def test_using_out_of_range_offset(self):
        response = self.get_comments(self.stored_articles[0].slug, 40)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            response.data['errors']['comments'],
            RESPONSE['not_found'].format(data="Comments")
        )

    def test_using_valid_data(self):
        response = self.get_comments(self.stored_articles[0].slug, 0)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['comment'],
            RESPONSE['comment']['get_success']
        )
