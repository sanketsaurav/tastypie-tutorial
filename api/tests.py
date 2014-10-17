from core import models
from tastypie.models import ApiKey
from tastypie.test import ResourceTestCase

from django.contrib.auth.models import User


class QuoteResourceTest(ResourceTestCase):

    def setUp(self):

        super(QuoteResourceTest, self).setUp()

        # Create a new user with profile
        self.user = User.objects.create_user(username='jonsnow',
            password='iknownothing')
        self.user_profile = models.Profile.objects.create(user=self.user,
            verified=True, bio='Foo bar!')
        self.user_profile.save()

        # Create a new author
        self.author = models.Author.objects.create(name='Albus Dumbledore',
            country='England')
        self.author.save()

        # Create an API key for the user
        self.user_api_key = ApiKey.objects.create(user=self.user)
        self.user_api_key.save()

        # Initialize details

        self.resource_name = 'quote'
        self.resource_uri = '/api/v1/{0}'.format(self.resource_name)

        # Seed data

        self.post_data = {
            'author' : '/api/v1/author/{0}'.format(self.author.slug),
            'quote' : 'It is not our abilities that make us who we are. It is our choices.',
            'creator' : '/api/v1/user/{0}'.format(self.user.username)
        }

        self.patch_data = {
            'quote' : 'Trust Harry. He is our only hope.',
        }

    def get_credentials(self):

        return self.create_apikey(self.user, self.user_api_key.key)

    def test_post_list_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.post(self.resource_uri,
            format='json', data=self.post_data))

    def test_post_list(self):
        old_count = models.Quote.objects.count()

        self.assertHttpCreated(self.api_client.post(self.resource_uri,
            format='json', data=self.post_data,
            authentication=self.get_credentials()))

        self.assertEqual(models.Quote.objects.count(), old_count + 1)

    def test_get_list_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(self.resource_uri,
                format='json'))

    def test_get_list(self):
        resp = self.api_client.get(self.resource_uri, format='json',
            authentication=self.get_credentials())

        # Check validity of JSON
        self.assertValidJSONResponse(resp)

        # Check if the length of data is valid
        self.assertEqual(len(self.deserialize(resp)['objects']),
            models.Quote.objects.count())