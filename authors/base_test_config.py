import json

# local imports
from authors.apps.authentication.models import User
from authors.apps.authentication.token import account_activation_token
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker

from rest_framework.test import APIClient

from .factory import (ArticleFactory, CommentFactory, CommentHistoryFactory,
                      UserFactory)

faker = Faker()


class TestConfiguration(TestCase):
    """ Configurations for all test suites"""

    # This flag is used to check whether a setup function has been
    # executed or not.
    set_up_done = False

    @classmethod
    def setUpClass(cls):
        """ Configurations for entire test suite """

        # This check to see if any other setup class function has been
        # executed.
        if not cls.set_up_done:

            # This executes the setUpClass function in the class we have
            # inherited from. This is to ensure we have not discarded the
            # default instructions from executing.
            super(TestConfiguration, cls).setUpClass()

            # This is to get the Django API test client to mock client
            # user requests to our backend.
            cls.client = APIClient()

            # This ensures we execute this function once for each class.
            cls.set_up_done = True

            try:

                # This is to ensure that database transactions are executed
                # successfully and sequentially.
                with transaction.atomic():

                    # This generates and saves the test data that we shall
                    # use in the test case scenarios.
                    cls.generate_test_data()

            except IntegrityError:
                pass

    @classmethod
    def generate_test_data(cls):

        # This generates a new user without saving to the database. We
        # store it in this variable, so we have access to this user's
        # details in the test cases.
        cls.stored_user = UserFactory.build(password="janedoe.T5")

        users = [
            {
                "email": cls.stored_user.email,
                "username": cls.stored_user.username,
                "password": cls.stored_user.password,
            },
            {
                "email": "johndoe@email.com",
                "username": "johndoe",
                "password": "johndoe.T5",
            }
        ]

        cls.stored_users = []

        for new_user in users:
            # We create a new user in order to ensure that we have control
            # over setting the activation status of the user, as well as
            # generating the hashed password.
            current_user = User(
                username=new_user['username'],
                email=new_user['email'],
                password=new_user['password']
            )

            current_user.set_password(cls.stored_user.password)
            current_user.is_active = True
            current_user.save()

            cls.stored_users.append(current_user)

        user = cls.stored_users[0]

        # This generates a new article with the author of the article
        # as the user we have just created. We store it in this variable,
        # so we have access to the article details in the test cases.
        cls.stored_articles = ArticleFactory.create_batch(
            50,
            author=user
        )

        article = ArticleFactory(
            author=user,
            body=faker.sentence(nb_words=200)
        )

        cls.stored_articles.append(article)

        # This block of code generates a couple of comments, in which the
        # latter block are reply comments of the first comment we generate.
        # These comments are commenting the article we have jsut created,
        cls.stored_comments = CommentFactory.create_batch(
            6,
            parent=0,
            user=user,
            article=cls.stored_articles[0]
        )

        cls.stored_comments.append(
            CommentFactory.create_batch(
                6,
                parent=cls.stored_comments[0].id,
                user=user,
                article=cls.stored_articles[0]
            )
        )

        cls.stored_comment_histories = CommentHistoryFactory.create_batch(
            4,
            comment=cls.stored_comments[0]
        )

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

        self.registered_user_email = {
            "user": {
                "email": "johndoe@email.com"
            }
        }

        self.reg_user = {
            "user": {
                "email": "johndoe11@email.com",
                "username": "johndoe11",
                "password": "johndoe.T5"
            }
        }

        self.reg_user2 = {
            "user": {
                "email": "johndoe12@email.com",
                "username": "johndoe12",
                "password": "johndoe.T5"
            }
        }

        self.log_user = {
            "user": {
                "email": "johndoe11@email.com",
                "password": "johndoe.T5"
            }
        }

        self.log_user2 = {
            "user": {
                "email": "johndoe12@email.com",
                "password": "johndoe.T5"
            }
        }

        self.invalid_username = "malone"

        self.update_profile = {
            "bio": "Coder",
            "image": "https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/512x512/plain/user.png",
            "company": "Call Of Duty",
            "website": "https://gabino.com",
            "location": "cape Town",
            "phone": "079000000"
        }

        self.article = {
            "article": {
                "title": "javascript es6",
                "description": "introduction to es6",
                "body": "intermedaite js developers"
            }
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

        activate_url = '/api/activate/account/{pk}/{token}'.format(
            pk=pk, token=token)
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


class TestUsingLoggedInUser(TestConfiguration):
    """
    This class is a subclass of the main TestConfiguration Class. It
    configures the test cases that require a logged in user.
    """

    access_token = ""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_login({
            "email": cls.stored_user.email,
            "password": cls.stored_user.password,
        })

    @classmethod
    def user_login(cls, user):
        """
        This function is responsible for retrieving the access token
        required to prove the user has been logged in.
        """

        data = {"user": user}

        response = cls.client.post(
            reverse("user_login"),
            json.dumps(data),
            content_type='application/json'
        )

        # This saves the access token we receive into a variable we can
        # access in the test cases.
        cls.access_token = response.data['token']
        cls.refresh_token = response.data['refresh_token']
