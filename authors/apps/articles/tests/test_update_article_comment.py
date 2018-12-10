from rest_framework import status
from django.urls import reverse

from authors.base_test_config import TestUsingLoggedInUser
from authors.response import RESPONSE


class TestUpdateArticleComment(TestUsingLoggedInUser):

    def setUp(self):
        super().setUp()
        self.comment = {
            "text": "This is a test comment."
        }

    def update_comment(self, comment_id, data):
        return self.client.put(
            reverse(
                "article_comment",
                kwargs={
                    "pk": comment_id,
                    "slug": self.stored_articles[0].slug
                }
            ),
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION="Token {}".format(self.access_token)
        )

    def test_using_no_text_field(self):
        self.comment.pop('text')

        response = self.update_comment(self.stored_comments[0].id, self.comment)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.data['errors']['text'],
            RESPONSE['no_field'].format('text')
        )

    def test_using_empty_text_field(self):
        self.comment['text'] = ""

        response = self.update_comment(self.stored_comments[1].id, self.comment)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.data['errors']['text'],
            RESPONSE['empty_field'].format('text')
        )

    def test_using_unexisting_comment_id(self):
        response = self.update_comment(999, self.comment)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            str(response.data['detail']),
            RESPONSE['default']['not_found']
        )

    def test_using_valid_data(self):
        response = self.update_comment(self.stored_comments[0].id, self.comment)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['user']['comment'],
            RESPONSE['comment']['update_success']
        )
