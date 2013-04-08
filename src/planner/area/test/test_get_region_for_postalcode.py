from __future__ import absolute_import
from unittest import TestCase
from planner.main.test.__init__ import RegionFactory
from nose.plugins.attrib import attr
from planner.area.models import Interval, Region
from planner.area.views import get_region_for_postcalcode, get_regions_for_postcalcode


@attr('functional', 'postalcode')
class GetRegionFromPostalcodeTest(TestCase):

    def setUp(self):
        Region.objects.all().delete()
        
        self.region = RegionFactory(name='Zuid-Oost', description='Zuid-Oost')
        self.region_east = RegionFactory(name='Oost', description='Oost')
        self.interval = Interval(begin='1000ab',
                                 end='1001sd',
                                 region=self.region)
        self.interval.save()
        self.interval_east = Interval(begin='1001aa',
                                 end='1001sd',
                                 region=self.region_east)
        self.interval_east.save()
    
    def tearDown(self):
        Region.objects.all().delete()
           
        
    def doPostcodeTest(self, code, expected_string):
        regions = get_region_for_postcalcode(code)
        assert expected_string in str(regions) 


    def testInTwoAreas(self):
        regions = get_regions_for_postcalcode("1001CC")
        assert self.region in regions
        assert self.region_east in regions
        
    def testUnknown(self):
        """ tests an unkown postalcode """
        self.doPostcodeTest("5000AD", 'Unknown')
        

    def testZuidOost(self):
        """ tests a known postalcode in Zuid-Oost """
        self.doPostcodeTest("1000AC", 'Zuid-Oost')

    def testZuidOost2(self):
        """ tests a known postalcode in Zuid-Oost 2"""
        self.doPostcodeTest("1000AB", 'Zuid-Oost')

    def testZuidOost3(self):
        """ tests a known postalcode in Zuid-Oost 3"""
        self.doPostcodeTest("1000SD", 'Zuid-Oost')

    def testZuidOost4(self):
        """ tests a known postalcode in Zuid-Oost small case"""
        self.doPostcodeTest("1000sd", 'Zuid-Oost')

    def testZuidOost5(self):
        """ tests a known postalcode in Zuid-Oost small case 2"""
        self.doPostcodeTest("1000ac", 'Zuid-Oost')
