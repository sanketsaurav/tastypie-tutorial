from django.conf.urls import patterns, include, url
from django.conf import settings

from tastypie.api import Api

from api import views

# Define API with version
v1_api = Api(api_name='v1')

# Register resources

v1_api.register(views.UserResource())
v1_api.register(views.QuoteResource())
v1_api.register(views.AuthorResource())
v1_api.register(views.ProfileResource())


urlpatterns = patterns('',
    url(r'', include(v1_api.urls)),
)
