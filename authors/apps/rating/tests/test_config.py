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
        self.user = {
            "user": {
                "email": "johndoe@email.com",
                "username": "johndoe",
                "password": "johndoe.T5",
            }
        }

        self.new_user = {
            "user": {
                "email": "johndoe2@email.com",
                "username": "johndoe2",
                "password": "johndoe.T5",
            }
        }
        self.new_user2 = {
            "user": {
                "email": "johndoe3@email.com",
                "username": "johndoe3",
                "password": "johndoe.T53",
            }
        }
        self.registered_user_email = {
            "user": {
                "email": "johndoe@email.com"
            }
        }
        self.activated_user = {
            "user": {
                "email": "johndoe2@email.com",
                "password": "johndoe.T5",
            }
        }
        self.activated_user2 = {
            "user": {
                "email": "johndoe3@email.com",
                "password": "johndoe.T53",
            }
        }
