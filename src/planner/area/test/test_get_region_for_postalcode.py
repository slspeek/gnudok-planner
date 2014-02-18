from __future__ import absolute_import
from unittest import TestCase
from planner.main.test.__init__ import RegionFactory
from nose.plugins.attrib import attr
from planner.main.models import Region
from planner.area.models import Interval
from planner.area.views import get_regions_for_postcalcode

import logging

@attr('functional', 'postalcode')
class GetRegionFromPostalcodeTest(TestCase):

    def setUp(self):
        Region.objects.all().delete()
        
        self.region = RegionFactory(name='Zuid-Oost', description='Zuid-Oost')
        self.interval = Interval(begin='1000ab',
                                 end='1001sd',
                                 region=self.region)
        self.interval.save()
        self.interval2 = Interval(begin='1000ab',
                                 end='1000ab',
                                 region=self.region)
        self.interval2.save()

        self.region_east = RegionFactory(name='Oost', description='Oost')
        self.interval_east = Interval(begin='1001aa',
                                 end='1001sd',
                                 region=self.region_east)
        self.interval_east.save()
    
    def tearDown(self):
        Region.objects.all().delete()
           
        
    def doPostcodeTest(self, code, expected_string):
        logging.info("All regions: %s " % Region.objects.all())
        regions = get_regions_for_postcalcode(code)
        logging.info("Regions: %s " % regions)
        assert expected_string in str(regions) 

    def testNoDoubleRegions(self):
        """ No doubles """
        regions = get_regions_for_postcalcode('1000ab')
        assert 1 == len(regions)

    def testInTwoAreas(self):
        regions = get_regions_for_postcalcode("1001CC")
        assert self.region in regions
        assert self.region_east in regions
        
    def testUnknown(self):
        """ tests an unkown postalcode """
        self.doPostcodeTest("5000AD", '')
        

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

@attr('functional', 'postalcode')
class GetRegionFromPostalcodeBoundsTest(TestCase):
    """ Bounds checks for get_regions_for_postcalcode """

    def setUp(self):
        Region.objects.all().delete()
        
        self.region = RegionFactory(name='Zuid-Oost', description='Zuid-Oost')
        self.interval = Interval(begin='1000ab',
                                 end='1001sd',
                                 region=self.region)
        self.interval.save()
    
    def tearDown(self):
        Region.objects.all().delete()
           
    def testLeftBoundIsInclusive(self):
        """ Left bound inclusive """
        regions = get_regions_for_postcalcode('1000ab')
        logging.info("Bound test regions: %s " % regions)
        assert 1 == len(regions)

    def testLeftBoundIsInclusiveUppercase(self):
        """ Left bound inclusive, uppercase """
        regions = get_regions_for_postcalcode('1000AB')
        logging.info("Bound test regions: %s " % regions)
        assert 1 == len(regions)

    def testRightBoundIsInclusive(self):
        """ Right bound inclusive """
        regions = get_regions_for_postcalcode('1001sd')
        logging.info("Bound test regions: %s " % regions)
        assert 1 == len(regions)

    def testRightBoundIsInclusiveUppercase(self):
        """ Right bound inclusive, uppercase """
        regions = get_regions_for_postcalcode('1001SD')
        logging.info("Bound test regions: %s " % regions)
        assert 1 == len(regions)
