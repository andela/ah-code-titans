
from rest_framework import status

# local imports
# from .test_config import TestConfiguration
from ..models import Profile
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
        self.register(
            self.reg_user)  # register a new user
        new_count = Profile.objects.count()
        self.assertNotEqual(initial_count, new_count)

    def test_get_user_profile(self):
        """
        Test user can get profile
        """

        self.email_verification(data=self.reg_user)
        res = self.login(data=self.log_user)
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
