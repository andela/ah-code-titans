# from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from ..models import User
from authors.apps.authentication.token import account_activation_token


class TestFollowUnfollowUser(TestCase):

    def register_user(self, user):
        """
        Register a user
        :param user:
        :return:
        """
        return self.client.post(
            reverse("create_user"),
            user,
            content_type='application/json'
        )

    def email_verification(self, user):
        """
        Login a user
        :param user:
        :return:
        """
        self.register_user(user)
        user_details = User.objects.get(username=user['user']['username'])
        pk = urlsafe_base64_encode(force_bytes(user_details.id)).decode()
        token = account_activation_token.make_token(user)

        activate_url = 'http://localhost:8000/api/activate/account/{pk}/{token}'.format(
            pk=pk, token=token
        )
        self.client.get(
            activate_url,
            content_type='application/json'
        )
        return

    def login(self, user):
        self.email_verification(user)
        response = self.client.post(
            reverse('user_login'),
            user,
            content_type='application/json'
        )
        return response.data

    followed = {
        'user': {
            'username': 'Johndoe',
            'password': 'JohnDoe@32',
            'email': 'johndoe@email.com'
        }
    }

    follower = {
        'user': {
            'username': 'Janedoe',
            'password': 'JaneDoe@32',
            'email': 'janedoe@email.com'
        }
    }

    def setUp(self):
        super(TestFollowUnfollowUser, self).setUp()
        self.email_verification(self.followed)
        logged_in = self.login(user=self.follower)
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + logged_in['token']
        )

    def test_following_existing_user(self):
        """
        Test for following an existing user
        :return:
        """
        response = self.client.post(
            reverse(
                'follow',
                kwargs={'username': self.followed['user'].get('username')}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_un_following_existing_user(self):
        """
        Test for un-following an existing user
        :return:
        """
        response = self.client.delete(
            reverse(
                'follow',
                kwargs={'username': self.followed['user'].get('username')}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_following_non_existing_user(self):
        """
        Test for following a non-existing user
        :return:
        """
        response = self.client.post(
            reverse(
                'follow',
                kwargs={'username': 'NotThere'}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unfollowing_non_existing_user(self):
        """
        Test for unfollowing a non-existing user
        :return:
        """
        response = self.client.delete(
            reverse(
                'follow',
                kwargs={'username': 'NotThere'}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_following_yourself(self):
        """
        Test for following yourself
        :return:
        """
        response = self.client.post(
            reverse(
                'follow',
                kwargs={'username': self.follower['user'].get('username')}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_unfollowing_yourself(self):
        """
        Test for unfollowing yourself
        :return:
        """
        response = self.client.delete(
            reverse(
                'follow',
                kwargs={'username': self.follower['user'].get('username')}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_view_followers(self):
        """
        Test for viewing followers
        :return:
        """
        response = self.client.get(
            reverse('followers')
        )
        self.assertIn(b'followers', response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_those_you_follow(self):
        """
        Test for viewing those you follow
        :return:
        """
        response = self.client.get(
            reverse('following')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_following_existing_user_not_authenticated(self):
        """
        Test for following an existing user
        :return:
        """
        self.client.credentials()
        response = self.client.post(
            reverse(
                'follow',
                kwargs={'username': self.followed['user'].get('username')}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unfollowing_existing_user_not_authenticated(self):
        """
        Test for following an existing user
        :return:
        """
        self.client.credentials()
        response = self.client.delete(
            reverse(
                'follow',
                kwargs={'username': self.followed['user'].get('username')}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
