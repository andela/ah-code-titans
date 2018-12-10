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
