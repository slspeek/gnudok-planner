"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from __future__ import absolute_import
import datetime
import factory
from django.test import TestCase
from django.test.client import Client
from nose.plugins.attrib import attr
from planner.nlpostalcode.models import Source, Country, Province, City,\
    Cityname, Postcode, Street
from planner.nlpostalcode.views import  get_streets


class SourceFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = Source
    id = factory.Sequence(lambda n: n)
    name = source = factory.Sequence(lambda n: "username%s" % n)
    created = updated = datetime.datetime.now()


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = Country

    id = factory.Sequence(lambda n: n)
    created = updated = datetime.datetime.now()
    name = factory.Sequence(lambda n: "Nederland%s" % n)
    source = factory.SubFactory(SourceFactory)


class ProvinceFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = Province

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "Provincie:%s" % n)
    created = updated = datetime.datetime.now()
    country = factory.SubFactory(CountryFactory)
    source = factory.SubFactory(SourceFactory)


class CityFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = City

    id = factory.Sequence(lambda n: n)
    created = updated = datetime.datetime.now()
    province = factory.SubFactory(ProvinceFactory)
    source = factory.SubFactory(SourceFactory)


class CitynameFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = Cityname

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "Amsterdam:%s" % n)
    created = updated = datetime.datetime.now()
    city = factory.SubFactory(CityFactory)
    source = factory.SubFactory(SourceFactory)


class PostcodeFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = Postcode

    id = factory.Sequence(lambda n: n)
    fourpp = 1056
    created = updated = datetime.datetime.now()
    city = factory.SubFactory(CityFactory)
    source = factory.SubFactory(SourceFactory)

class StreetFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = Street

    id = factory.Sequence(lambda n: n)
    even = factory.Sequence(lambda n: 2 * n)
    created = updated = datetime.datetime.now()
    street = "Pieter van der Doesstraat"
    postcode = factory.SubFactory(PostcodeFactory)
    chars = "VE"
    source = factory.SubFactory(SourceFactory)

class SimpleTest(TestCase):

    def setUp(self):
        """ sets up a Django test client """
        self.client = Client()

        builder = PostcodeBuilder()
        self.postcode = builder.create_amsterdam_postcode_number(1056)
        self.street = builder.create_street(self.postcode, "Pieter van der Doesstraat", 've')
        self.street = builder.create_street(self.postcode, "Pieter van der Doesstraat 2", 'vx')
        assert len(Street.objects.all()) == 2
        streets = Street.objects.filter(postcode__fourpp=1056).filter(chars='ve')
        assert len(streets.all()) == 1


    def test_postcode_lookup(self):
        response = self.client.get("/pc/get/1056ve")
        assert "Pieter van der Doesstraat" in response.content


class PostcodeBuilder(object):

    def __init__(self):
        self.country = CountryFactory()
        self.province = ProvinceFactory(country=self.country)
        self.city = CityFactory(province=self.province)
        self.cityname = CitynameFactory(city=self.city, name='Amsterdam')

    def create_amsterdam_postcode_number(self, four_digit_number):
        postcode = PostcodeFactory(fourpp=four_digit_number, city=self.city)
        return postcode

    def create_street(self, postcode, name, two_letters):
        # pylint: disable=R0201
        street = StreetFactory(postcode=postcode, chars=two_letters, street=name)
        return street

@attr('update')
class UpdateTest(TestCase):

    def setUp(self):
        """ sets up a Django test client """
        self.client = Client()
        Street.objects.all().delete()
        builder = PostcodeBuilder()
        self.postcode = builder.create_amsterdam_postcode_number(1057)
        self.street = builder.create_street(self.postcode, "Pieter van der Doesstraat", 've')
        self.street = builder.create_street(self.postcode, "Pieter van der Doesstraat 2", 'vx')
        assert len(Street.objects.all()) == 2
        streets = Street.objects.filter(postcode__fourpp=1057).filter(chars='ve')
        assert len(streets.all()) == 1



    def test_get_streets(self):
        # pylint: disable=R0201
        street = get_streets(1057, 've')
        assert len(street.all()) == 1
        s = street[0]
        assert s.street == "Pieter van der Doesstraat"
