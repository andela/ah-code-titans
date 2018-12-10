from django.test import TestCase


class TestConfig(TestCase):
    """ Configurations for all tests"""

    article_data = {
        "article": {
            "title": "javascript es6",
            "description": "introduction to es6",
            "body": "intermediate js developers"
        }
    }
    article_data_2 = {
        "article": {
            "title": "javascript es7",
            "description": "introduction to es7",
            "body": "intermediate js developers"
        }
    }
