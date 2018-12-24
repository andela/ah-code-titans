
from rest_framework import status
from django.urls import reverse

# local imports
from authors.apps.bookmark.models import Bookmark
from authors.base_test_config import TestUsingLoggedInUser

from authors.response import RESPONSE


class TestBookmark(TestUsingLoggedInUser):
    """
    Test bookmarking functionality
    """

    def post_article(self, data):
        response = self.client.post(
            reverse('articles'),
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION="Token {}".format(self.access_token)
        )
        return response

    def test_user_cannot_bookmark_un_existing_articles(self):
        """
        Test user cannot bookmark or unbookmark article that do not exist
        """

        self.post_article(self.article)
        slug = "bookmark"

        response = self.client.post(
            '/api/article/{slug}/bookmark'.format(slug=slug),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )
        response2 = self.client.delete(
            '/api/article/{slug}/bookmark'.format(slug=slug),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        self.assertIn(response.data['message'], RESPONSE['article_not_found'].format(data=slug))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(response2.data['message'], RESPONSE['article_not_found'].format(data=slug))
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_bookmark_model(self):
        """"
        test model can create user profile upon successful sign up
        """

        initial_count = Bookmark.objects.count()
        res2 = self.post_article(self.article)
        slug = res2.data['slug']
        
        self.client.post(
            '/api/article/{slug}/bookmark'.format(slug=slug),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )
        new_count = Bookmark.objects.count()
        self.assertNotEqual(initial_count, new_count)

    def test_user_can_bookmark_article(self):
        """
        Test user can bookmark an article
        """

        res2 = self.post_article(self.article)
        slug = res2.data['slug']

        response = self.client.post(
            '/api/article/{slug}/bookmark'.format(slug=slug),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        response2 = self.client.post(
            '/api/article/{slug}/bookmark'.format(slug=slug),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        self.assertIn(response.data['message'], RESPONSE['bookmark']['bookmarked'].format(data=slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response2.data['message'], RESPONSE['bookmark']['repeat_bookmarking'])
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_unbookmark_article(self):
        """
        Test user can unfbookmark an article
        """

        res2 = self.post_article(self.article)
        slug = res2.data['slug']

        self.client.post(
            '/api/article/{slug}/bookmark'.format(slug=slug),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )
        response = self.client.delete(
            '/api/article/{slug}/bookmark'.format(slug=slug),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        response2 = self.client.delete(
            '/api/article/{slug}/bookmark'.format(slug=slug),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        self.assertIn(response.data['message'], RESPONSE['bookmark']['unbookmarked'].format(data=slug))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn(response2.data['message'], RESPONSE['bookmark']['repeat_unbookmarking'])
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_retrive_bookmarked_articles(self):
        """
        Test user can retrive all bookmarked articles
        """

        res2 = self.post_article(self.article)
        slug = res2.data['slug']
        response = self.client.get(
            '/api/articles/all/bookmarks',
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        self.client.post(
            '/api/article/{slug}/bookmark'.format(slug=slug),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )
        response2 = self.client.get(
            '/api/articles/all/bookmarks',
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
