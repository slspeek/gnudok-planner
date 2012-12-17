"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from __future__ import absolute_import
from django.test import TestCase
from django.test.client import Client
from .models import Source, Country, Province, City, Cityname, Postcode, Street
import datetime
import factory

    
class SourceFactory(factory.Factory):
    FACTORY_FOR = Source
    id = factory.Sequence(lambda n: n)
    name = source = factory.Sequence(lambda n: "username%s" % n)
    created = updated = datetime.datetime.now()


class CountryFactory(factory.Factory):
    FACTORY_FOR = Country
    
    id = 0
    created = updated = datetime.datetime.now()
    name = "Nederland"
    source = factory.SubFactory(SourceFactory)
    

class ProvinceFactory(factory.Factory):
    FACTORY_FOR = Province
    
    id = 0
    name = "Noord-Holland"
    created = updated = datetime.datetime.now()
    country = factory.SubFactory(CountryFactory)
    source = factory.SubFactory(SourceFactory)
    

class CityFactory(factory.Factory):
    FACTORY_FOR = City
    
    id = 0
    created = updated = datetime.datetime.now()
    province = factory.SubFactory(ProvinceFactory)
    source = factory.SubFactory(SourceFactory)


class CitynameFactory(factory.Factory):
    FACTORY_FOR = Cityname
    
    id = 0
    name = 'Amsterdam'
    created = updated = datetime.datetime.now()
    city = factory.SubFactory(CityFactory)
    source = factory.SubFactory(SourceFactory)


class PostcodeFactory(factory.Factory):
    FACTORY_FOR = Postcode
    
    id = factory.Sequence(lambda n: n)
    fourpp = 1056
    created = updated = datetime.datetime.now()
    city = factory.SubFactory(CityFactory)
    source = factory.SubFactory(SourceFactory)

class StreetFactory(factory.Factory):
    FACTORY_FOR = Street

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
        streets  = Street.objects.filter(postcode__fourpp=1056).filter(chars='ve')
        assert len(streets.all()) == 1
        
        
    def test_postcode_lookup(self):
        response = self.client.get("/pc/get/1056ve")
        assert "Pieter van der Doesstraat" in response.content
             
             
class PostcodeBuilder(object):
    
    def __init__(self):
        self.country = CountryFactory()
        self.province = ProvinceFactory(country=self.country)
        self.city = CityFactory(province=self.province)
        self.cityname = CitynameFactory(city=self.city,name='Amsterdam')
    
    def create_amsterdam_postcode_number(self, four_digit_number):
        postcode = PostcodeFactory(fourpp=four_digit_number, city=self.city)
        return postcode
    
    def create_street(self, postcode, name, two_letters):
        street = StreetFactory(postcode=postcode, chars=two_letters, street=name)
        return street
        