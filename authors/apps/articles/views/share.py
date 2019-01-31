import os

from rest_framework.response import Response
from rest_framework import status, generics, exceptions
from rest_framework.permissions import IsAuthenticated

from django.urls import reverse
from django_social_share.templatetags import social_share

from ..models import Article
from authors.response import RESPONSE


class ShareArticleView(generics.RetrieveAPIView):
    """
    This class hosts the endpoints that handle the article sharing feature for
    authenticated users.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Share aricle endpoint

        This endpoint returns a share link for authenticated users. The user shall
        be able to redirect to the specified share url.
        """

        # This gets the provider specified in the url.
        provider = kwargs['provider']

        context = {"request": request}

        # This tries to fetch an article from the database by using the slug provided
        # in the url parameter(kwargs). If the article slug provided does not match
        # any in the database, an error 404 response is sent back to the API user.
        try:
            article = Article.objects.get(slug=kwargs['slug'])

        except Article.DoesNotExist:
            raise exceptions.NotFound({
                "errors": {
                    "article": RESPONSE['not_found'].format(data="Article")
                }
            })

        # This builds a link for a user on a social media website to redirect to the
        # specified article on the Authors Haven platform.
        article_url = request.build_absolute_uri(
            "{}article/{}".format(
                os.getenv("FRONTEND"),
                article.slug
            )
        )

        share_link = self.get_link(context, provider, article, article_url)

        if not share_link:
            # When the endpoint user provides a non-specified provider for sharing, we
            # handle this by returning an error message stating that what has been
            # provided is invalid.
            return Response(
                {
                    "errors": {
                        "provider": RESPONSE['invalid_field'].format("provider")
                    }
                }, status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "share": {
                    "link": share_link,
                    "provider": provider
                }
            }, status.HTTP_200_OK
        )

    def get_link(self, context, provider, article, article_url):
        share_link = None

        if provider == "facebook":
            # This gets the share link for a user to redirect to the facebook platform.
            share_link = social_share.post_to_facebook_url(
                context,
                article_url
            )['facebook_url']

        elif provider == "twitter":
            text = "Check this out at Authors Haven: {}".format(
                article.title)

            # This gets the share link for a user to redirect to the twitter platform.
            share_link = social_share.post_to_twitter(
                context,
                text,
                article_url,
                link_text='Post to Twitter'
            )['tweet_url']

        elif provider == "reddit":
            # This gets the share link for a user to redirect to the reddit platform.
            share_link = social_share.post_to_reddit_url(
                context,
                article.title,
                article_url
            )['reddit_url']

        elif provider == "linkedin":
            title = "Check this out at Authors Haven : {}".format(
                article.title)

            # This gets the share link for a user to redirect to the linkedin platform.
            share_link = social_share.post_to_linkedin_url(
                context,
                title,
                article_url
            )['linkedin_url']

        elif provider == "email":
            text = "Check this out at Authors Haven: {}".format(article.title)
            subject = "Article from Authors Haven has been shared to you!"

            # This gets the share link for a user to redirect to the email platform.
            share_link = social_share.send_email_url(
                context,
                subject,
                text,
                article_url
            )['mailto_url']

        return share_link
