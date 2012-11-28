"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

class SimpleTest(TestCase):
    
    def setUp(self):
        """ sets up a Django test client """
        self.client = Client()
        
        
    def test_postcode_lookup(self):
         response = self.client.get("/pc/get/1056ve")
         assert "Pieter van der Doesstraat" in response.content
             
