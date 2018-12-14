from rest_framework import status
from django.urls import reverse

from authors.base_test_config import TestUsingLoggedInUser
from authors.response import RESPONSE


class TestDeleteArticleComment(TestUsingLoggedInUser):

    def delete_comment(self, comment_id):
        return self.client.delete(
            reverse(
                "article_comment",
                kwargs={
                    "pk": comment_id,
                    "slug": self.stored_articles[0].slug
                }
            ),
            HTTP_AUTHORIZATION="Token {}".format(self.access_token)
        )

    def test_using_unexisting_comment_id(self):
        response = self.delete_comment(999)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            str(response.data['detail']),
            RESPONSE['default']['not_found']
        )

    def test_using_valid_data(self):
        response = self.delete_comment(self.stored_comments[1].id)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['comment'],
            RESPONSE['comment']['delete_success']
        )
