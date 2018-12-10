from rest_framework import status
from django.urls import reverse

from authors.apps.articles.models import Article
from authors.base_test_config import TestConfiguration

slug = None


class TestLikeDislike(TestConfiguration):
    """
    Class to test for liking and disliking of articles.
    """
    def create_article(self):
        """
        Method to create an article first and return a token.
        """
        article = {
            "article": {
                "title": "How To Train Your Dragon",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian"
            }
        }
        # register the user and verify email
        self.email_verification(self.reg_user)

        # login the registered user
        response = self.login(self.log_user)

        # grab the token from the response data
        token = response.data["token"]

        # Create an article using the authentication token
        self.client.post(
            reverse("articles"),
            article,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        return token

    def test_article_like(self):
        """
        Test if an article can be liked.
        """
        # create an article and get user token
        token = self.create_article()

        # get the article slug
        article = Article.objects.all().first()
        global slug
        slug = article.slug

        # set the url
        url = '/api/articles/{}/like/'.format(slug)
        like_response = self.client.post(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        # Test for correct response
        self.assertEqual(like_response.status_code, status.HTTP_201_CREATED)

        # Test response data to see if the article has 1 like
        self.assertEqual(like_response.data["total_likes"], 1)

    def test_dislike_article(self):
        """
        Test if an article can be disliked
        """
        token = self.create_article()
        url = '/api/articles/{}/dislike/'.format(slug)

        like_response = self.client.post(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        # Test for correct response
        self.assertEqual(like_response.status_code, status.HTTP_201_CREATED)

        # Test response data to see if the article has 1 dislike
        self.assertEqual(like_response.data["total_dislikes"], 1)

    def test_for_already_liked_article(self):
        """
        Test deletion of vote.
        If a user likes an article they have already liked,
        the vote is removed
        """
        token = self.create_article()
        url = '/api/articles/{}/like/'.format(slug)

        # Post a like to the article
        self.client.post(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )

        # Like the article twice
        like_response = self.client.post(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        # Test for correct response
        self.assertEqual(like_response.status_code, status.HTTP_201_CREATED)

        # Test response data to see if the article has 0 likes
        self.assertEqual(like_response.data["total_likes"], 0)








