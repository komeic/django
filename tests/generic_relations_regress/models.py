from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


__all__ = ('Link', 'Place', 'Restaurant', 'Person', 'Address',
           'CharLink', 'TextLink', 'OddRelation1', 'OddRelation2',
           'Contact', 'Organization', 'Note', 'Company')

@python_2_unicode_compatible
class Link(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    def __str__(self):
        return "Link to %s id=%s" % (self.content_type, self.object_id)

@python_2_unicode_compatible
class Place(models.Model):
    name = models.CharField(max_length=100)
    links = generic.GenericRelation(Link)

    def __str__(self):
        return "Place: %s" % self.name

@python_2_unicode_compatible
class Restaurant(Place):
    def __str__(self):
        return "Restaurant: %s" % self.name

@python_2_unicode_compatible
class Address(models.Model):
    street = models.CharField(max_length=80)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    def __str__(self):
        return '%s %s, %s %s' % (self.street, self.city, self.state, self.zipcode)

@python_2_unicode_compatible
class Person(models.Model):
    account = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    addresses = generic.GenericRelation(Address)

    def __str__(self):
        return self.name

class CharLink(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=100)
    content_object = generic.GenericForeignKey()

class TextLink(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.TextField()
    content_object = generic.GenericForeignKey()

class OddRelation1(models.Model):
    name = models.CharField(max_length=100)
    clinks = generic.GenericRelation(CharLink)

class OddRelation2(models.Model):
    name = models.CharField(max_length=100)
    tlinks = generic.GenericRelation(TextLink)

# models for test_q_object_or:
class Note(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    note = models.TextField()

class Contact(models.Model):
    notes = generic.GenericRelation(Note)

class Organization(models.Model):
    name = models.CharField(max_length=255)
    contacts = models.ManyToManyField(Contact, related_name='organizations')

@python_2_unicode_compatible
class Company(models.Model):
    name = models.CharField(max_length=100)
    links = generic.GenericRelation(Link)

    def __str__(self):
        return "Company: %s" % self.name

# For testing #13085 fix, we also use Note model defined above
class Developer(models.Model):
    name = models.CharField(max_length=15)

@python_2_unicode_compatible
class Team(models.Model):
    name = models.CharField(max_length=15)
    members = models.ManyToManyField(Developer)

    def __str__(self):
        return "%s team" % self.name

    def __len__(self):
        return self.members.count()

class Guild(models.Model):
    name = models.CharField(max_length=15)
    members = models.ManyToManyField(Developer)

    def __nonzero__(self):
        return self.members.count()

class Tag(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='g_r_r_tags')
    object_id = models.CharField(max_length=15)
    content_object = generic.GenericForeignKey()
    label = models.CharField(max_length=15)

class Board(models.Model):
    name = models.CharField(primary_key=True, max_length=15)

class HasLinks(models.Model):
    links = generic.GenericRelation(Link)

    class Meta:
        abstract = True

class HasLinkThing(HasLinks):
    pass
