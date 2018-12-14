from rest_framework import status
from django.urls import reverse

from authors.base_test_config import TestConfiguration
from authors.response import RESPONSE


class TestGetCommentReplies(TestConfiguration):

    def get_replies(self, comment_id, offset):
        return self.client.get(
            reverse(
                "article_comment_replies",
                kwargs={
                    "pk": comment_id,
                    "slug": self.stored_articles[0].slug,
                    "offset": offset
                }
            )
        )

    def test_using_unexisting_comment_id(self):
        response = self.get_replies(999, 0)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            response.data['errors']['comments'],
            RESPONSE['not_found'].format(data="Comments")
        )

    def test_using_out_of_range_offset(self):
        response = self.get_replies(self.stored_comments[0].id, 40)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            response.data['errors']['comments'],
            RESPONSE['not_found'].format(data="Comments")
        )

    def test_using_valid_data(self):
        response = self.get_replies(self.stored_comments[0].id, 0)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['comment'],
            RESPONSE['comment']['replies']['get_success']
        )
