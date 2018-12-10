
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# local imports
# from authors.apps.profiles.tests.test_config import TestConfiguration
from authors.apps.authentication.models import User
from authors.apps.authentication.token import account_activation_token


from rest_framework.test import APIClient
from django.test import TestCase


class TestConfiguration(TestCase):
    """ Configurations for all tests"""

    @classmethod
    def setUpClass(cls):
        """ Configurations for entire test suite """
        super(TestConfiguration, cls).setUpClass()
        cls.client = APIClient()

    def setUp(self):
        """ Configurations for test cases """
        self.reg_user = {
            "user": {
                "email": "johndoe@email.com",
                "username": "johndoe",
                "password": "johndoe.T5"
            }
        }

        self.reg_user2 = {
            "user": {
                "email": "johndoe2@email.com",
                "username": "johndoe2",
                "password": "johndoe.T5"
            }
        }

        self.log_user = {
            "user": {
                "email": "johndoe@email.com",
                "password": "johndoe.T5"
            }
        }

        self.log_user2 = {
            "user": {
                "email": "johndoe2@email.com",
                "password": "johndoe.T5"
            }
        }

        self.update_profile = {
            "bio": "Coder",
            "image": "https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/512x512/plain/user.png",
            "company": "Call Of Duty",
            "website": "gabino.com",
            "location": "cape Town",
            "phone": "079000000"
        }

    def register(self, data):
        """
        register a user
        """
        self.client.post(
            reverse("create_user"),
            data,
            content_type='application/json'
        )

    def email_verification(self, data):
        """
        Verify registered user
        """

        self.register(data)
        user_details = User.objects.get(username=data['user']['username'])
        pk = urlsafe_base64_encode(force_bytes(user_details.id)).decode()
        token = account_activation_token.make_token(self.reg_user)

        activate_url = '/api/activate/account/{pk}/{token}'.format(pk=pk, token=token)
        self.client.get(
            activate_url,
            content_type='application/json'
        )

    def login(self, data):
        """
        login a user
        """
        res = self.client.post(
            reverse("user_login"),
            data,
            content_type='application/json'
        )
        return res
