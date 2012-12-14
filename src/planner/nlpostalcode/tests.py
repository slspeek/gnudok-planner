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
    id = 0
    name = source = 'foo'
    created = updated = datetime.datetime.now()


class CountryFactory(factory.Factory):
    FACTORY_FOR = Country
    
    id = 0
    created = updated = datetime.datetime.now()
    name = "Nederland"
    

class ProvinceFactory(factory.Factory):
    FACTORY_FOR = Province
    
    id = 0
    name = "Noord-Holland"
    created = updated = datetime.datetime.now()
    country = factory.SubFactory(CountryFactory)
    

class CityFactory(factory.Factory):
    FACTORY_FOR = City
    
    id = 0
    created = updated = datetime.datetime.now()
    province = factory.SubFactory(ProvinceFactory)


class CitynameFactory(factory.Factory):
    FACTORY_FOR = Cityname
    
    id = 0
    name = 'Amsterdam'
    created = updated = datetime.datetime.now()
    city = factory.SubFactory(CityFactory)


class PostcodeFactory(factory.Factory):
    FACTORY_FOR = Postcode
    
    id = 0
    fourpp = 1056
    created = updated = datetime.datetime.now()
    city = factory.SubFactory(CityFactory)

class StreetFactory(factory.Factory):
    FACTORY_FOR = Street

    id = 0
    even = 0
    created = updated = datetime.datetime.now()
    street = "Pieter van der Doesstraat"
    postcode = factory.SubFactory(PostcodeFactory)
    chars = "VE"

class SimpleTest(TestCase):
    
    def setUp(self):
        """ sets up a Django test client """
        self.client = Client()
        self.source = SourceFactory()
        self.country = CountryFactory(id=0,source=self.source)
        self.province = ProvinceFactory(id=0,source=self.source,country=self.country)
        self.city = CityFactory(id=0, source=self.source, province=self.province)
        self.cityname = CitynameFactory(id=0,source=self.source,city=self.city,name='Amsterdam')
        self.postcode = PostcodeFactory(id=0, source=self.source, fourpp=1056, city=self.city)
        self.street = StreetFactory(id=0, postcode=self.postcode, source=self.source, chars='ve', street="Pieter van der Doesstraat")
        assert len(Street.objects.all()) == 1
        streets  = Street.objects.filter(postcode__fourpp=1056).filter(chars='ve')
        assert len(streets.all()) == 1
        
        
    def test_postcode_lookup(self):
         response = self.client.get("/pc/get/1056ve")
         assert "Pieter van der Doesstraat" in response.content
             
