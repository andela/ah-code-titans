from rest_framework import status
from django.urls import reverse

from authors.base_test_config import TestUsingLoggedInUser


class TestGetCommentHistory(TestUsingLoggedInUser):

    def get_replies(self, comment_id):
        response = self.client.get(
            reverse(
                "comment_edit_history",
                kwargs={
                    "pk": comment_id
                }
            ),
            content_type='application/json',
            HTTP_AUTHORIZATION="Token {}".format(self.access_token)
        )

        return response

    def test_using_unexisting_comment_id(self):
        response = self.get_replies(999)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['results'],
            []
        )

    def test_using_valid_data(self):
        response = self.get_replies(self.stored_comments[0].id)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertNotEqual(
            response.data['results'],
            []
        )
