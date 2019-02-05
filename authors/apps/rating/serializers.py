import numpy

from django.db.models import Sum, Q

from rest_framework import serializers
from rest_framework import exceptions

# local imports
from .models import RateArticle
from ..articles.models import Article


class RateArticleSerializer(serializers.Serializer):

    class Meta:
        model = RateArticle
        fields = ['user_rating', 'article_id', 'user_id']

    def get_article_to_rate(self, slug):
        """
        Method to check if the article to be rated exists
        """
        to_rate = Article.objects.filter(slug=slug)
        # import pdb; pdb.set_trace()
        # find the article the user wants to rate. If not found return 404
        if not to_rate:
            raise exceptions.NotFound({
                "message": "Article was not found"
            })
        return Article.objects.get(slug=slug)

    @staticmethod
    def get_rating_per_article(slug):
        """
        Method to get user rating as per the article
        """
        # Check if article exists
        rated = RateArticleSerializer().get_article_to_rate(slug=slug)

        # Second perform a check if there is an article that has the article id
        # in the rating table. Proceed to find the number of users who have rated the article
        # find the sum of those ratings
        # return back the average to the user.
        # If no rating matching the article id exists return 0 to user
        # import pdb; pdb.set_trace()
        if RateArticle.objects.filter(article_id=rated.id).exists():
            # find the total number of users
            number_of_users = RateArticle.objects.filter(article_id=rated.id).values('user_id').count()

            # get all ratings of this article
            article_rates = RateArticle.objects.filter(article_id=rated.id).values('user_rating').aggregate(Sum('user_rating')).get('user_rating__sum')
            # import pdb; pdb.set_trace()
            return (numpy.rint(article_rates / number_of_users))
        return 0

    @staticmethod
    def rate_article(data, user_id, article_id):
        """
        Method to rate an article
        """

        my_rate = data.get('rate', None)

        # Validate that user has entered an integer
        if type(my_rate) is not int:
            raise serializers.ValidationError(
                'Rate value should be a number thats 1 to 5'
            )
        # Validate that the rate is not None and Must be between 1 to 5
        elif my_rate is None or my_rate not in range(1, 6):
            raise serializers.ValidationError(
                'Please rate the article with a number between 1 to 5'
            )
        # Restrict article owner from rating themselves
        elif Article.objects.filter(author_id=user_id, id=article_id).exists():
            raise exceptions.PermissionDenied(
                "You cannot rate your own article")

        # Check if the user has already rated the article. If so find the instance that matches
        # the user id and article id. To the value that exists as user rating pass in the new rating.
        # update the column in the database. If user has never rated the article before. Create the
        # new rating as per the user
        if RateArticle.objects.filter(user_id=user_id, article_id=article_id).exists():
            to_rate = RateArticle.objects.get(
                Q(user_id=user_id),
                Q(article_id=article_id)
            )
            # pass in the new rating
            to_rate.user_rating = my_rate

            to_rate.save(update_fields=['user_rating'])
            return {
                "rating": my_rate
            }

        # create the rating
        rate = RateArticle.objects.create(
            user_rating=my_rate,
            article_id=article_id,
            user_id=user_id)
        rate.save()

        return rate
