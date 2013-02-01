from __future__ import absolute_import
from django.test.client import Client
from django.test.testcases import TestCase
from planner.main.test.__init__ import RegionFactory
from nose.plugins.attrib import attr
from planner.area.models import Interval


@attr('functional', 'postalcode')
class GetRegionFromPostalcodeTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        """ sets up a Django test client """
        self.client = Client()
        self.region = RegionFactory(name='Zuid-Oost', description='Zuid-Oost')
        self.interval = Interval(begin='1000ab',
                                 end='1001sd',
                                 region=self.region)
        self.interval.save()

    def testUnknown(self):
        """ tests an unkown postalcode """
        response = self.client.get("/area/postalcode/5000AD")
        assert 'Unknown' in response.content

    def testZuidOost(self):
        """ tests a known postalcode """
        response = self.client.get("/area/postalcode/1000AC")
        assert 'Zuid-Oost' in response.content

    def testZuidOost2(self):
        """ tests a known postalcode """
        response = self.client.get("/area/postalcode/1000AB")
        assert 'Zuid-Oost' in response.content

    def testZuidOost3(self):
        """ tests a known postalcode """
        response = self.client.get("/area/postalcode/1000SD")
        assert 'Zuid-Oost' in response.content

    def testZuidOost4(self):
        """ tests a known postalcode """
        response = self.client.get("/area/postalcode/1000sd")
        assert 'Zuid-Oost' in response.content

    def testZuidOost5(self):
        """ tests a known postalcode """
        response = self.client.get("/area/postalcode/1000ac")
        assert 'Zuid-Oost' in response.content
