import factory

from authors.apps.articles.models import Article, Comment, CommentHistory
from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile
from faker import Faker

faker = Faker()


def generate_username(*args):
    """ returns a random username """

    fake = Faker()
    return fake.profile(fields=['username'])['username']


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.LazyAttribute(generate_username)
    email = factory.Faker('email')

    class Meta:
        model = User


class UserProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    bio = factory.Faker("sentence", nb_words=25)
    company = factory.Faker("company")
    website = factory.Faker("hostname")
    location = factory.Faker("city")
    phone = factory.Faker("phone_number")

    class Meta:
        model = Profile


class ArticleFactory(factory.django.DjangoModelFactory):

    author = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraph', nb_sentences=3)
    body = factory.Faker('text', max_nb_chars=10000)

    class Meta:
        model = Article


class CommentFactory(factory.django.DjangoModelFactory):

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
    text = factory.Faker("sentence", nb_words=25)

    class Meta:
        model = Comment


class CommentHistoryFactory(factory.django.DjangoModelFactory):

    comment = factory.SubFactory(CommentFactory)
    text = factory.Faker("sentence", nb_words=25)

    class Meta:
        model = CommentHistory
