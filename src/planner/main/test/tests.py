'''
Test module
'''
from __future__ import absolute_import
from .__init__ import *
from planner.main.models import Region, TimeSlot, Calendar, Appointment, Customer, Rule, Car
from planner.main.schedule import get_rules, get_or_create_calendar
from planner.main.views import get_date_from_iso
import datetime
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from nose.plugins.attrib import attr

@attr('functional')
class GetOrCreateCalendar(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.timeslot = TimeSlotFactory()
        self.region = RegionFactory()
        self.car = CarFactory()
        self.rule = RuleFactory(car=self.car,region=self.region,timeslot=self.timeslot)
        self.date = datetime.date(2012, 10, 29)
        self.calendar = CalendarFactory(date=self.date, car=self.car, timeslot=self.timeslot)

    def test_one_filled(self):
        result = get_or_create_calendar(self.timeslot.pk,self.car.pk,  self.date)
        self.assertEqual(1, len(Calendar.objects.all()))
        assert result == self.calendar
        
        
@attr('functional')       
class TestRulesForRegion(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.timeslot = TimeSlotFactory()
        self.region = RegionFactory()
        self.car = CarFactory()
        self.rule = RuleFactory(car=self.car,region=self.region,timeslot=self.timeslot)

    def test_one_filled(self):
        self.date = datetime.date(2012, 10, 29)
        result = get_rules(self.date, self.region)
        self.assertEqual(1, len(result))

    def test_empty(self):
        self.date = datetime.date(2012, 10, 25)
        result = get_rules(self.date, self.region)
        self.assertEqual(0, len(result))


@attr('unit')
class TestIsoDate(TestCase):

    def test_from_iso_date(self):
        self.assertEqual(datetime.date(2012, 10, 2), get_date_from_iso('20121002'))


@attr('functional')
class CalendarNoDoublesTest(TestCase):
    
    def test_no_doubles(self):
        rule = RuleFactory()
        def create_calendar():
            CalendarFactory.create( timeslot=rule.timeslot, car=rule.car)
        create_calendar()
        self.assertRaises(Exception,create_calendar)
        assert len(Calendar.objects.all()) == 1
