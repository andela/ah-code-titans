import random

from django.core.management.base import BaseCommand
from faker import Faker
from django.db.utils import IntegrityError

from authors.factory import (
    ArticleFactory,
    CommentFactory,
    CommentHistoryFactory,
    UserFactory,
    UserProfileFactory
)

faker = Faker()


class Command(BaseCommand):
    help = 'Generate API test data'

    def handle(self, *args, **kwargs):
        # This generates a new user without saving to the database. We
        # store it in this variable, so we have access to this user's
        # details in the test cases.
        new_user = UserFactory.build(
            email="johndoe@email.com",
            username="johndoe",
            password="janedoe.T5"
        )

        new_users = [new_user]
        new_users += UserFactory.build_batch(12)
        stored_users = []

        for user in new_users:
            # We create a new user in order to ensure that we have control
            # over setting the activation status of the user, as well as
            # generating the hashed password.

            user.set_password(user.password)
            try: 
                user.save()
            except IntegrityError:
                print("{} user already exists!".format(user.username))
                continue

            profile = UserProfileFactory.build()

            user.profile.bio = profile.bio
            user.profile.website = profile.website
            user.profile.image = profile.image
            user.profile.company = profile.company
            user.profile.location = profile.location
            user.profile.phone = profile.phone
            user.profile.save()

            stored_users.append(user)

        user = stored_users[0]

        # This generates a new article with the author of the article
        # as the user we have just created. We store it in this variable,
        # so we have access to the article details in the test cases.
        stored_articles = ArticleFactory.create_batch(
            50,
            author=random.choice(stored_users)
        )

        article = ArticleFactory(
            author=user,
            body=faker.paragraphs(nb=25)
        )

        stored_articles.append(article)

        # This block of code generates a couple of comments, in which the
        # latter block are reply comments of the first comment we generate.
        # These comments are commenting the article we have jsut created,
        
        TAGS = [
            "CULTURE",
            "MUSIC",
            "TECH",
            "ART",
            "STARTUPS",
            "SELF",
            "POLITICS",
            "DESIGN",
            "HEALTH",
            "SCIENCE"
        ]

        for article in stored_articles:

            article.tag_list.add(random.choice(TAGS).lower())
            article.tag_list.add(random.choice(TAGS).lower())
            article.save()

            stored_comments = CommentFactory.create_batch(
                3,
                parent=0,
                user=random.choice(stored_users),
                article=article
            )

            stored_comments.append(
                CommentFactory.create_batch(
                    3,
                    parent=stored_comments[0].id,
                    user=random.choice(stored_users),
                    article=article
                )
            )

            CommentHistoryFactory.create_batch(
                4,
                comment=stored_comments[0]
            )
