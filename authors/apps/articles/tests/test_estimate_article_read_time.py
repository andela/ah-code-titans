from django.urls import reverse

from rest_framework import status

from authors.base_test_config import TestUsingLoggedInUser


class TestEstimatedArticleReadTime(TestUsingLoggedInUser):

    def create_article(self, data):

        response = self.client.post(
            reverse("articles"),
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token {}'.format(self.access_token))

        return response

    def retrieve_article(self, slug):
        return self.client.get(
            reverse(
                "article",
                kwargs={
                    "slug": slug
                }),
            content_type='application/json')

    def test_article_time_to_read(self):
        """
        Test to get the time to read of an article
        """
        data = {
            "article": {
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": str(self.stored_articles[50].body)
            }
        }
        create_test_article = self.create_article(data)
        response = self.retrieve_article(
            create_test_article.data['slug']
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['time_to_read'], 2)
