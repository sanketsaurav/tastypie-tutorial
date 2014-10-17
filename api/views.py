from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization

from django.contrib.auth.models import User

from core import models
from api.custom import CustomModelResource


class UserResource(CustomModelResource):
    
    class Meta(CustomModelResource.Meta):

        queryset = User.objects.all()
        resource_name = 'user'
        detail_uri_name = 'username'
        authorization = DjangoAuthorization()

class QuotrResource(CustomModelResource):

    bio = fields.CharField(attribute='bio')
    city = fields.CharField(attribute='city')
    dob = fields.DateField(attribute='dob')
    verified = fields.BooleanField(attribute='verified')
    
    class Meta(CustomModelResource.Meta):

        queryset = User.objects.all()
        resource_name = 'quotr'
        detail_uri_name = 'username'
        authorization = DjangoAuthorization()

class QuoteResource(CustomModelResource):

    author = fields.ToOneField('api.views.AuthorResource',
        'author', full=True)

    creator = fields.ToOneField('api.views.UserResource',
        'creator', full_list=False, full_detail=True, full=True)
    
    class Meta(CustomModelResource.Meta):

        queryset = models.Quote.objects.all()
        resource_name = 'quote'
        detail_uri_name = 'uid'
        authorization = DjangoAuthorization()

class AuthorResource(CustomModelResource):
    
    class Meta(CustomModelResource.Meta):

            queryset = models.Author.objects.all()
            resource_name = 'author'
            detail_uri_name = 'slug'
            authorization = DjangoAuthorization() 