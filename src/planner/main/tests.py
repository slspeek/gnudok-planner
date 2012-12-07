'''
Test module
'''
from __future__ import absolute_import
from .models import Region, TimeSlot, Calendar, Appointment, Customer, Rule, Car
from .schedule import get_free_count, get_rules, get_or_create_calendar
from .views import get_free_entries, get_date_from_iso
import datetime
from django.contrib.auth.models import User
import factory
from django.test.testcases import TestCase
from nose.plugins.attrib import attr


class CarFactory(factory.Factory):
    FACTORY_FOR = Car
    
    name = "Open source tractor"
    
    
class TimeSlotFactory(factory.Factory):
    FACTORY_FOR = TimeSlot

    day_of_week = 1
    begin = 13
    end = 17


class RegionFactory(factory.Factory):
    FACTORY_FOR = Region

    name = "Groot Oost"

class RuleFactory(factory.Factory):
    FACTORY_FOR = Rule
    
    car = factory.SubFactory(CarFactory)
    region = factory.SubFactory(RegionFactory)
    timeslot = factory.SubFactory(TimeSlotFactory)
    
    

class CustomerFactory(factory.Factory):
    FACTORY_FOR = Customer

    name = "Willem Knaap"
    address = "Grachtengordel 1"
    town = "Juinen"
    postcode = "1469 SH"
    phone = "020-6164590"
    email = "wk@example.com"


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = "nancy"
    password = "nancy-secret"


class CalendarFactory(factory.Factory):
    FACTORY_FOR = Calendar

    date = datetime.date(2012, 10, 29)
    timeslot = factory.SubFactory(TimeSlotFactory)
    car = factory.SubFactory(CarFactory)
    #region = factory.SubFactory(RegionFactory)


class AppointmentFactory(factory.Factory):
    FACTORY_FOR = Appointment

    calendar = factory.SubFactory(CalendarFactory)
    customer = factory.SubFactory(CustomerFactory)
    employee = factory.SubFactory(UserFactory)
    stuff = "Gold, Platina and lots of Silver"
    notes = "Bring boxes"
    created = datetime.datetime.now()

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
