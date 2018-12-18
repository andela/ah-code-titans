
from rest_framework import status
from django.urls import reverse

# local imports
from ..models import FavouriteArticle
from authors.base_test_config import TestUsingLoggedInUser


class TestProfile(TestUsingLoggedInUser):
    """
    Test profile functionality
    """

    def post_article(self, data):
        response = self.client.post(
            reverse('articles'),
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION="Token {}".format(self.access_token)
        )
        return response

    def test_favorite_model_creates_an_instanse(self):
        """"
        test model can create user profile upon successful sign up
        """

        initial_count = FavouriteArticle.objects.count()
        res2 = self.post_article(self.article)
        slug = res2.data['slug']

        url = '/api/article/{slug}/favorite'.format(slug=slug)
        self.client.post(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )
        new_count = FavouriteArticle.objects.count()
        self.assertNotEqual(initial_count, new_count)

    def test_user_can_favorite_article(self):
        """
        Test user can favorite an article
        """

        res2 = self.post_article(self.article)
        slug = res2.data['slug']

        url = '/api/article/{slug}/favorite'.format(slug=slug)
        response = self.client.post(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        response2 = self.client.post(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        self.assertIn(response.data['message'], 'You have favorited this article')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response2.data['message'], 'You have already favorited this article')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_unfavorite_article(self):
        """
        Test user can unfavorite an article
        """

        res2 = self.post_article(self.article)
        slug = res2.data['slug']

        url = '/api/article/{slug}/favorite'.format(slug=slug)
        self.client.post(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )
        response = self.client.delete(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        response2 = self.client.delete(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        self.assertIn(response.data['message'], 'You have unfavorited this article')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn(response2.data['message'], 'You have already unfavorited this article')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_get_favorited_articles(self):
        """
        Test user can get all favorited articles
        """

        res2 = self.post_article(self.article)
        slug = res2.data['slug']

        url = '/api/articles/all/favorites'
        response = self.client.get(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )
        self.client.post(
            '/api/article/{slug}/favorite'.format(slug=slug),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )
        response2 = self.client.get(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        self.assertIn(response.data['message'], 'You have not favorited any articles')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_user_cannot_favorited_un_existing_articles(self):
        """
        Test user cannot favorite or unfavorite article that do not exist
        """

        self.post_article(self.article)
        slug = "scrrr"

        url = '/api/article/{slug}/favorite'.format(slug=slug)
        response = self.client.post(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )
        response2 = self.client.delete(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

        self.assertIn(response.data['message'], 'Article {slug} was not found'.format(slug=slug))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(response2.data['message'], 'Article {slug} was not found'.format(slug=slug))
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
