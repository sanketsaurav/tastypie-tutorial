from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication, \
                    ApiKeyAuthentication, MultiAuthentication


class CustomModelResource(ModelResource):

    class Meta:

        excludes = ['id', 'password', 'is_staff', 'is_active', 'is_superuser']
        serializer = Serializer(formats=['json'])
        # authentication = MultiAuthentication(SessionAuthentication(), 
        #                     ApiKeyAuthentication())
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'patch', 'delete']
        max_limit = 100