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


class TestNoAppointmentsOnCalendar(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.rule = RuleFactory()

    def test_get_free_count(self):
        date = datetime.date(2012, 10, 29)
        result = get_free_count(date, self.rule)
        self.assertEqual(4, result, "Expected 4 free places")


class TestAppointmentCalendarPresent(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.car = CarFactory()
        self.timeslot = TimeSlotFactory()
        self.rule = RuleFactory(car=self.car, timeslot=self.timeslot)
        self.appointment = AppointmentFactory.create(
            calendar__car=self.car,
            calendar__timeslot=self.timeslot)
        self.date = datetime.date(2012, 10, 29)

    def test_get_free_count(self):
        result = get_free_count(self.date, self.rule)
        self.assertEqual(3, result, "Expected 3 free places left")


class TestGetFreeEntries(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.rule = RuleFactory()
        self.date = datetime.date(2012, 10, 29)
        self.appointment = AppointmentFactory.create(calendar__car=self.rule.car,
                                                     calendar__timeslot=self.rule.timeslot)

    def test_get_free_entries(self):
        result = get_free_entries(self.date, 21, self.rule.region)
        self.assertEqual(3, len(result))

    def test_get_free_entries_two_weeks(self):
        result = get_free_entries(self.date, 14, self.rule.region)
        self.assertEqual(2, len(result))


class TestIsoDate(TestCase):

    def test_from_iso_date(self):
        self.assertEqual(datetime.date(2012, 10, 2), get_date_from_iso('20121002'))


class CalendarNoDoublesTest(TestCase):
    
    def test_no_doubles(self):
        rule = RuleFactory()
        def create_calendar():
            CalendarFactory.create( timeslot=rule.timeslot, car=rule.car)
        create_calendar()
        self.assertRaises(Exception,create_calendar)
        assert len(Calendar.objects.all()) == 1
