import factory
from authors.apps.articles.models import Article, Comment
from authors.apps.authentication.models import User
from faker import Faker


def generate_username(*args):
    """ returns a random username """

    fake = Faker()
    return fake.profile(fields=['username'])['username']


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.LazyAttribute(generate_username)
    email = factory.Faker('email')

    class Meta:
        model = User


class ArticleFactory(factory.django.DjangoModelFactory):

    author = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraphs', nb=1)
    body = factory.Faker('paragraphs', nb=5)

    class Meta:
        model = Article


class CommentFactory(factory.django.DjangoModelFactory):

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
    text = factory.Faker("sentence", nb_words=25)

    class Meta:
        model = Comment
