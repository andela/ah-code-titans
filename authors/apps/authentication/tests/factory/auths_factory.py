import factory
from ...models import User


class UserFactory(factory.Factory):
    """ generates user data """

    class Meta:
        model = User

    username = factory.Sequence(lambda n: "kimame%d" % n)
    email = factory.LazyAttribute(lambda b: "%s@gmail.com" % b.username)
    password = "password"
