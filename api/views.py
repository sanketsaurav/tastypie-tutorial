from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.utils import trailing_slash

from django.contrib.auth.models import User
from django.conf.urls import url

from core import models
from api.custom import CustomModelResource, QuoteAuthorization, \
    ProfileAuthorization, UserAuthorization


class UserResource(CustomModelResource):

    profile = fields.ToOneField('api.views.ProfileResource', 'profile',
         full=True)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>\w[\w/-]*)/quotes%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_user_quotes'), name="api_get_user_quotes"),
        ]

    def get_user_quotes(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)
        try:
            bundle = self.build_bundle(data={'username': kwargs['username']}, request=request)
            obj = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        quotes = QuoteResource()
        return quotes.get_list(request, creator__exact=obj)

    def dehydrate(self, bundle):

        bundle.data['total_quotes'] = bundle.obj.quotes.count()
        return bundle
    
    class Meta(CustomModelResource.Meta):

        queryset = User.objects.all()
        resource_name = 'user'
        detail_uri_name = 'username'
        authorization = UserAuthorization()

class ProfileResource(CustomModelResource):
    
    class Meta(CustomModelResource.Meta):

        queryset = models.Profile.objects.all()
        resource_name = 'profile'
        authorization = ProfileAuthorization()

class QuoteResource(CustomModelResource):

    author = fields.ToOneField('api.views.AuthorResource',
        'author', full=True)

    creator = fields.ToOneField('api.views.UserResource',
        'creator', full_list=False, full_detail=True, full=True)
    
    class Meta(CustomModelResource.Meta):

        queryset = models.Quote.objects.all()
        resource_name = 'quote'
        detail_uri_name = 'uid'
        authorization = QuoteAuthorization()
        filtering = {
            'creator' : ('exact',),
            'author' : ('exact',),
        }

class AuthorResource(CustomModelResource):

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<slug>\w[\w/-]*)/quotes%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_author_quotes'), name="api_get_author_quotes"),
        ]

    def get_author_quotes(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)
        try:
            bundle = self.build_bundle(data={'slug': kwargs['slug']}, request=request)
            obj = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        quotes = QuoteResource()
        return quotes.get_list(request, author__exact=obj)

    def dehydrate(self, bundle):
        
        bundle.data['total_quotes'] = bundle.obj.quotes.count()
        return bundle
    
    class Meta(CustomModelResource.Meta):

            queryset = models.Author.objects.all()
            resource_name = 'author'
            detail_uri_name = 'slug'
            authorization = DjangoAuthorization() 