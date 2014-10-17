import datetime
import uuid
import pytz

import hashids

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from core.utils import unique_slugify

class BaseModel(models.Model):
    """
    Base model class that provides common fields required by all other
    models.
    """

    created = models.DateTimeField(blank=True, null=True,
        default=datetime.datetime.utcnow())

    modified = models.DateTimeField(blank=True, null=True,
        default=datetime.datetime.utcnow())


    def save(self, *args, **kwargs):
        
        if not self.id:
            self.created = datetime.datetime.utcnow()
        self.modified = datetime.datetime.utcnow()

        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:

        abstract = True


class Quotr(BaseModel):
    """
    A user's profile.
    """

    user = models.OneToOneField(User, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    city =  models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.get_full_name()


class Quote(BaseModel):
    """
    A quote.
    """

    creator = models.ForeignKey(User, related_name='quotes')
    quote = models.TextField()
    author = models.ForeignKey('Author', related_name='quotes')
    uid = models.SlugField(unique=True, null=True, blank=True)

    def __unicode__(self):
        return self.quote

    def save(self, *args, **kwargs):

        super(Quote, self).save(*args, **kwargs)

        h = hashids.Hashids(salt=settings.HASHIDS_SALT,
            min_length=settings.HASHIDS_MIN_LENGTH, 
            alphabet=settings.HASHIDS_ALPHABET)
        
        self.uid = h.encrypt(self.id)

        return super(Quote, self).save(*args, **kwargs)


class Author(BaseModel):
    """
    Author of a quote.
    """

    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):

        unique_slugify(self, self.name)

        return super(Author, self).save(*args, **kwargs)