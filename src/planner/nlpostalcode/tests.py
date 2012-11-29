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
    name = source = 'foo'
    created = updated = datetime.datetime.now()

class SourceFactoryImpl(object):
    
    def __init__(self):
        self.id = 0
    
    def create(self):
        self.id += 1
        name = str(self.id)
        source = str(self.id)
        return SourceFactory(id=self.id, name=name, source=source)
                       
source_factory = SourceFactoryImpl()

class CountryFactory(factory.Factory):
    FACTORY_FOR = Country
    
    id = 0
    created = updated = datetime.datetime.now()
    name = "Nederland"
    #source = source_factory.create()
#    
#
#class ProvinceFactory(factory.Factory):
#    FACTORY_FOR = Province
#    
#    id = 0
#    name = "Noord-Holland"
#    created = updated = datetime.datetime.now()
#    source = source_factory.create()
#    country = factory.SubFactory(CountryFactory)
#    
#
#class CityFactory(factory.Factory):
#    FACTORY_FOR = City
#    
#    id = 0
#    created = updated = datetime.datetime.now()
#    province = factory.SubFactory(ProvinceFactory)
#    source = source_factory.create()
#
#
#class CitynameFactory(factory.Factory):
#    FACTORY_FOR = Cityname
#    
#    id = 0
#    name = 'Amsterdam'
#    created = updated = datetime.datetime.now()
#    source = source_factory.create()
#    city = factory.SubFactory(CityFactory)
#
#
#class PostcodeFactory(factory.Factory):
#    FACTORY_FOR = Postcode
#    
#    id = 0
#    fourpp = 1056
#    created = updated = datetime.datetime.now()
#    source = source_factory.create()
#    city = factory.SubFactory(CityFactory)
#
#class StreetFactory(factory.Factory):
#    FACTORY_FOR = Street
#
#    id = 0
#    created = updated = datetime.datetime.now()
#    street = "Pieter van der Doesstraat"
#    postcode = factory.SubFactory(PostcodeFactory)
#    source = source_factory.create()
#    chars = "VE"

class SimpleTest(TestCase):
    
    def setUp(self):
        """ sets up a Django test client """
        self.client = Client()
        
#        self.foo = source_factory.create()
#        self.bar = source_factory.create()
#        self.goo = source_factory.create()
        self.country = CountryFactory()
        #self.street = ProvinceFactory.create()
        #self.street = CitynameFactory.create()
        #self.street = CityFactory.create()
        #self.street = PostcodeFactory.create()
        
        
    def test_postcode_lookup(self):
         response = self.client.get("/pc/get/1056ve")
         assert "Pieter van der Doesstraat" in response.content
             
