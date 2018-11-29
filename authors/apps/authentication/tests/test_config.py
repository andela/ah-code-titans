from rest_framework.test import APIClient
from django.test import TestCase

from .test_data import generate_test_data


class TestConfiguration(TestCase):
    """ Configurations for all tests"""

    @classmethod
    def setUpClass(cls):
        """ Configurations for entire test suite """
        super(TestConfiguration, cls).setUpClass()
        cls.client = APIClient()
        generate_test_data()

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
