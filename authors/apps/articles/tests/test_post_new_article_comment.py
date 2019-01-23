from rest_framework import status
from django.urls import reverse

from authors.base_test_config import TestUsingLoggedInUser
from authors.response import RESPONSE


class TestPostNewArticleComment(TestUsingLoggedInUser):

    def setUp(self):
        super().setUp()
        self.comment = {
            "parent": 0,
            "text": "This is a test comment."
        }

    def post_comment(self, data, slug):
        return self.client.post(
            reverse(
                "article_comments",
                kwargs={
                    "slug": slug
                }
            ),
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION="Token {}".format(self.access_token)
        )

    def test_using_no_text_field(self):
        self.comment.pop('text')

        response = self.post_comment(
            self.comment, self.stored_articles[0].slug)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            str(response.data['errors']['text'][0]),
            RESPONSE['default']['no_field']
        )

    def test_using_empty_text_field(self):
        self.comment['text'] = ""

        response = self.post_comment(
            self.comment, self.stored_articles[0].slug)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            str(response.data['errors']['text'][0]),
            RESPONSE['default']['empty_field']
        )

    def test_using_no_parent_field(self):
        self.comment.pop('parent')

        response = self.post_comment(
            self.comment, self.stored_articles[0].slug)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            str(response.data['errors']['parent'][0]),
            RESPONSE['default']['no_field']
        )

    def test_using_invalid_parent_id(self):
        self.comment['parent'] = 'ro'

        response = self.post_comment(
            self.comment, self.stored_articles[0].slug)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            str(response.data['errors']['parent'][0]),
            RESPONSE['default']['invalid_field']['int']
        )

    def test_using_unexisting_article_slug(self):
        response = self.post_comment(self.comment, "does-not-exist")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            str(response.data['detail']),
            RESPONSE['default']['not_found']
        )

    def test_using_valid_data(self):
        response = self.post_comment(
            self.comment, self.stored_articles[0].slug)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data['comment'],
            RESPONSE['comment']['post_success']
        )
