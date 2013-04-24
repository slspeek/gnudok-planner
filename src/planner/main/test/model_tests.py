'''
Created on 7 jan. 2013

@author: steven
'''
from __future__ import absolute_import
from .__init__ import CustomerFactory
from unittest import TestCase
from nose.plugins.attrib import attr

@attr('model', 'unit')
class CustomerAddresss(TestCase):

    def test_address_display_with_addition(self):
        customer = CustomerFactory(address='Mainstreet', number='42', additions='2nd floor' )
        self.assertEqual("Mainstreet 42 - 2nd floor", customer.get_address_display())
        
    def test_address_display_without_addition(self):
        customer = CustomerFactory(address='Mainstreet', number='42')
        self.assertEqual("Mainstreet 42", customer.get_address_display())