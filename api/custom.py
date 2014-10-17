from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import SessionAuthentication, \
                    ApiKeyAuthentication, MultiAuthentication
from tastypie.exceptions import Unauthorized


class CustomModelResource(ModelResource):

    class Meta:

        excludes = ['id', 'password', 'is_staff', 'is_active', 'is_superuser',
            'last_login']
        serializer = Serializer(formats=['json'])
        # authentication = MultiAuthentication(SessionAuthentication(), 
        #                     ApiKeyAuthentication())
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        max_limit = 100

class QuoteAuthorization(Authorization):

    """
    Permissions:
        VIEW:       Anyone
        EDIT:       Owner
        DELETE:     Owner
        CREATE:     Owner
    """

    def read_list(self, object_list, bundle):        
        return object_list

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        user = bundle.request.user        
        return object_list.filter(creator=user)           

    def create_detail(self, object_list, bundle):
        user = bundle.request.user
        return bundle.obj.creator == user            

    def update_list(self, object_list, bundle):
        user = bundle.request.user        
        return object_list.filter(creator=user) 

    def update_detail(self, object_list, bundle):
        user = bundle.request.user
        return bundle.obj.creator == user

    def delete_list(self, object_list, bundle):
        raise Unauthorized()

    def delete_detail(self, object_list, bundle):
        user = bundle.request.user
        return bundle.obj.creator == user

class UserAuthorization(Authorization):

    """
    Permissions:
        VIEW:       Anyone
        EDIT:       Owner
        DELETE:     None
        CREATE:     None
    """

    def read_list(self, object_list, bundle):        
        return object_list

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        raise Unauthorized()           

    def create_detail(self, object_list, bundle):
        user = bundle.request.user
        return bundle.obj == user            

    def update_list(self, object_list, bundle):
        raise Unauthorized() 

    def update_detail(self, object_list, bundle):
        user = bundle.request.user
        return bundle.obj == user

    def delete_list(self, object_list, bundle):
        raise Unauthorized()

    def delete_detail(self, object_list, bundle):
        raise Unauthorized()

class ProfileAuthorization(UserAuthorization):

    def create_detail(self, object_list, bundle):
        user = bundle.request.user
        return bundle.obj.user == user

    def update_detail(self, object_list, bundle):
        user = bundle.request.user
        return bundle.obj.user == user