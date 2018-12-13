from rest_framework import status
from ...articles.models import Article
from .test_data import test_article, test_rate
from .test_rate_article import TestRateArticle


class TestGetArticleRating(TestRateArticle):

    def test_get_initial_rating(self):
        """
        Test on initial article rating before any is done
        """
        self.email_verification_and_login_user1()
        self.create_article(test_article[0])
        test_article_slug = Article.objects.all()

        response = self.client.get(
            "/api/article/{slug}/rating".format(slug=test_article_slug[0].slug),
            content_type='application/json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json().get('Rated at'),
            0
        )

    def test_get_user_rating(self):
        """
        Test to get actual user rating on an article
        """
        self.email_verification_and_login_user1()
        token = self.email_verification_and_login_user2()

        self.create_article(test_article[0])
        test_article_slug = Article.objects.all()

        self.client.post(
            "/api/article/{slug}/rate".format(slug=test_article_slug[0].slug),
            test_rate[1],
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        response = self.client.get(
            "/api/article/{slug}/rating".format(slug=test_article_slug[0].slug),
            content_type='application/json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json().get('Rated at'),
            5
        )

    def test_none_existing_article(self):
        """
        Test to get actual user rating on an article
        """
        self.email_verification_and_login_user1()
        token = self.email_verification_and_login_user2()

        self.create_article(test_article[0])
        test_article_slug = Article.objects.all()
        slug = test_article_slug[0].slug + 'll'

        self.client.post(
            "/api/article/{slug}/rate".format(slug=slug),
            test_rate[1],
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        response = self.client.get(
            "/api/article/{slug}/rating".format(slug=slug),
            content_type='application/json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
