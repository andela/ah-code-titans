from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import status
from ...authentication.models import User
from ...articles.models import Article
from .test_config import TestConfiguration
from ...authentication.token import account_activation_token
from .test_data import test_rate, test_article

user_token = None
user_token2 = None
slug = None


class TestRateArticle(TestConfiguration):

    def register_user(self, data):
        """ method register a new user """
        return self.client.post(
            reverse("create_user"),
            data,
            content_type='application/json'
        )

    def login(self, data):
        """ method used to login a user """
        return self.client.post(
            reverse("user_login"),
            data,
            content_type='application/json'
        )

    def create_article(self, data):
        """
        Method to create article
        """
        token = user_token
        return self.client.post(
            reverse("articles"),
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )

    def email_verification_and_login_user1(self):
        """
        Method to register, verify and login a first user
        """
        self.register_user(self.new_user)
        user_details = User.objects.get(username=self.new_user['user']['username'])
        pk = urlsafe_base64_encode(force_bytes(user_details.id)).decode()
        token = account_activation_token.make_token(self.new_user)

        activate_url = 'http://localhost:8000/api/activate/account/{pk}/{token}'.format(pk=pk, token=token)
        self.client.get(
            activate_url,
            content_type='application/json'
        )
        test_token = self.login(self.activated_user)
        global user_token
        user_token = test_token.data['token']

        return test_token.data['token']

    def email_verification_and_login_user2(self):
        """
            Method to register, verify and login a second user
        """
        self.register_user(self.new_user2)
        user_details = User.objects.get(username=self.new_user2['user']['username'])
        pk = urlsafe_base64_encode(force_bytes(user_details.id)).decode()
        token = account_activation_token.make_token(self.new_user2)

        activate_url = 'http://localhost:8000/api/activate/account/{pk}/{token}'.format(pk=pk, token=token)
        self.client.get(
            activate_url,
            content_type='application/json'
        )
        test_token = self.login(self.activated_user2)
        global user_token2
        user_token2 = test_token.data.get('token')

        return test_token.data.get('token')

    def test_with_rate_as_string(self):
        """
        Test if user try to rate the article with a string
        """
        token = self.email_verification_and_login_user1()
        self.create_article(test_article[0])
        all_test = Article.objects.all()
        global slug
        slug = all_test[0].slug

        response = self.client.post(
            '/api/article/{slug}/rate'.format(slug=slug),
            test_rate[0],
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_with_rate_own_article(self):
        """
        Method to test whenuser tries to rate own article
        """
        token = self.email_verification_and_login_user1()
        self.create_article(test_article[0])

        response = self.client.post(
            "/api/article/{slug}/rate".format(slug=slug),
            test_rate[1],
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            response.json().get('detail'),
            'You cannot rate your own article'
        )

    def test_with_rate_greater_than_5(self):
        """
        Test if user try to rate the article with rate value greater than five
        """
        token = self.email_verification_and_login_user1()
        self.create_article(test_article[0])

        response = self.client.post(
            '/api/article/{slug}/rate'.format(slug=slug),
            test_rate[2],
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_with_user_create_rating(self):
        """
        Test on a different user rating another users article
        """
        self.email_verification_and_login_user1()
        token = self.email_verification_and_login_user2()

        self.create_article(test_article[0])

        response = self.client.post(
            "/api/article/{slug}/rate".format(slug=slug),
            test_rate[1],
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json().get('message'),
            "Successfully rated the article"
        )

    def test_with_user_edit_rating(self):
        """
        Test on user editing their own previous rate
        """
        self.email_verification_and_login_user1()
        token = self.email_verification_and_login_user2()

        self.create_article(test_article[0])
        self.client.post(
            "/api/article/{slug}/rate".format(slug=slug),
            test_rate[1],
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        response = self.client.post(
            "/api/article/{slug}/rate".format(slug=slug),
            test_rate[3],
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json().get('message'),
            "Successfully rated the article"
        )
