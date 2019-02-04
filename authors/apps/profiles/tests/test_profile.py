from django.urls import reverse

from rest_framework import status

# local imports
from authors.apps.profiles.models import Profile
from authors.base_test_config import TestConfiguration


class TestProfile(TestConfiguration):
    """
    Test profile functionality
    """

    def test_model_auto_create_user_profile(self):
        """"
        test model can create user profile upon successful sign up
        """

        initial_count = Profile.objects.count()
        self.register(self.reg_user)  # register a new user
        new_count = Profile.objects.count()
        self.assertNotEqual(initial_count, new_count)

    def test_get_user_profile(self):
        """
        Test user can get profile
        """

        self.email_verification(self.reg_user)
        res = self.login(self.log_user)
        username = res.data['username']
        token = res.data['token']
        url = '/api/profiles/' + username
        response = self.client.get(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_view_other_user_profile(self):
        """
        A user can view other user's profile
        """

        self.email_verification(self.reg_user)
        self.email_verification(self.reg_user2)
        res = self.login(self.log_user2)
        username = self.reg_user['user']['username']
        token = res.data['token']
        url = '/api/profiles/' + username
        response = self.client.get(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_user_profile(self):
        """
        Test 404 for invalid user
        """

        self.email_verification(self.reg_user)
        res = self.login(self.log_user)
        username = self.invalid_username
        token = res.data['token']
        url = '/api/profiles/' + username
        response = self.client.get(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        self.assertIn(response.data['detail'], 'User profile not found')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_not_edit_other_user_profile(self):
        """
        A user can not edit other user's profile
        """

        self.email_verification(self.reg_user)
        self.email_verification(self.reg_user2)
        res = self.login(self.log_user2)
        username = self.reg_user['user']['username']
        token = res.data['token']
        url = '/api/profiles/edit/' + username
        response = self.client.put(
            url,
            self.update_profile,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_profile(self):
        """
        Test authorised user can update own profile.
        """

        self.email_verification(self.reg_user)
        res = self.login(self.log_user)
        username = res.data['username']
        token = res.data['token']
        url = '/api/profiles/edit/' + username
        response = self.client.put(
            url,
            self.update_profile,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_authors(self):
        """
        Test getting a list of authors
        :return:
        """
        self.email_verification(self.reg_user)
        res = self.login(self.log_user)
        token = res.data['token']
        response = self.client.get(
            reverse('authors_profile'),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )

        self.assertEqual(
            response.data['results'][-1]['username'],
            self.reg_user['user']['username']
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_authors_unauthenticated(self):
        """
        Test getting all users when not logged in
        :return:
        """
        response = self.client.get(
            reverse('authors_profile'),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
