from django.urls import reverse

from rest_framework import status

from authors.base_test_config import TestUsingLoggedInUser
from authors.apps.articles.tests.test_config import TestConfig


class TestSearchFilter(TestUsingLoggedInUser, TestConfig):
    """
    Test class for search and filter
    """
    def create_article(self, data):
        """
        Method to create an article.
        We'll test search and filter on this article
        """
        response = self.client.post(
            reverse("articles"),
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token {}'.format(self.access_token)
        )

        return response.data['slug']

    def retrieve_article(self, slug):
        response = self.client.get(
            reverse(
                "article",
                kwargs={
                    "slug": slug
                }),
            content_type='application/json')
        return response.data

    def test_filter_article_title(self):
        """
        Method to test if articles can be filtered by title
        """
        self.create_article(self.article_data)
        response = self.client.get(
            '/api/search/articles/?title={}'.format(self.article_data['article']['title']),
            content_type='application/json')

        # Test response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test response data
        self.assertEqual(
            response.data['results'][0]['title'], self.article_data['article']['title'])

    def test_filter_article_author(self):
        """
        Method to test if articles can be filtered by author
        """
        slug = self.create_article(self.article_data)

        article = self.retrieve_article(slug=slug)

        response = self.client.get(
            '/api/search/articles/?author={}'.format(article['author']['username']),
            content_type='application/json')

        # Test response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test response data
        self.assertEqual(
            response.data['results'][0]['author']['username'], article['author']['username'])

    def test_search_article_keyword(self):
        """
        Method to test for article search by keyword
        """
        self.create_article(self.article_data)
        title_keyword = 'javascript'
        response = self.client.get(
            '/api/search/articles/?search={}'.format(title_keyword),
            content_type='application/json')

        # Test response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test response data
        self.assertIn(title_keyword, response.data['results'][0]['title'])

    def test_search_article_by_tag(self):
        """
        Method to test for article search by tag name
        """
        self.create_article(self.article_data)
        tag = self.article_data['article']['tag_list'][0]
        response = self.client.get(
            '/api/search/articles/?tags={}'.format(tag),
            content_type='application/json')

        # Test response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test response data
        self.assertIn(tag, response.data['results'][0]['tag_list'])
