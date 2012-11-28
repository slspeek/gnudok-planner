'''
Test module
'''
from __future__ import absolute_import
from .models import Region, TimeSlot, Calendar, Appointment, Customer
from .views import get_free_count, get_timeslots_for_day_of_week
from .views import get_timeslots, get_free_entries, get_date_from_iso
import datetime
from django.contrib.auth.models import User
import factory
from django.test.testcases import TestCase


class TimeSlotFactory(factory.Factory):
    FACTORY_FOR = TimeSlot

    day_of_week = 1
    begin = 13
    end = 17


class RegionFactory(factory.Factory):
    FACTORY_FOR = Region

    name = "Groot Oost"


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
    region = factory.SubFactory(RegionFactory)


class AppointmentFactory(factory.Factory):
    FACTORY_FOR = Appointment

    calendar = factory.SubFactory(CalendarFactory)
    customer = factory.SubFactory(CustomerFactory)
    employee = factory.SubFactory(UserFactory)
    stuff = "Gold, Platina and lots of Silver"
    notes = "Bring boxes"


class TestTimeslotsForRegion(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.timeslot1 = TimeSlotFactory.create()
        self.region = RegionFactory.create()
        self.region.timeslots.add(self.timeslot1)

    def test_one_filled(self):
        self.date = datetime.date(2012, 10, 29)
        result = get_timeslots(self.date, self.region)
        self.assertEqual(1, len(result))

    def test_empty(self):
        self.date = datetime.date(2012, 10, 25)
        result = get_timeslots(self.date, self.region)
        self.assertEqual(0, len(result))


class TestTimeslotsForDay(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.timeslot1 = TimeSlotFactory.create(day_of_week=1)
        self.timeslot2 = TimeSlotFactory.create(day_of_week=2)
        self.timeslot3 = TimeSlotFactory.create(day_of_week=3)
        self.timeslots = [self.timeslot1, self.timeslot2, self.timeslot3]

    def test(self):
        result = get_timeslots_for_day_of_week(1, self.timeslots)
        self.assertEqual(1, len(result))


class TestNoAppointmentsOnCalendar(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.region = RegionFactory.create()
        self.timeslot = TimeSlotFactory.create()

    def test_get_free_count(self):
        date = datetime.date(2012, 10, 29)
        result = get_free_count(date, self.timeslot, self.region)
        self.assertEqual(4, result, "Expected 4 free places")


class TestAppointmentCalendarPresent(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.region = RegionFactory.create()
        self.timeslot = TimeSlotFactory.create()
        self.appointment = AppointmentFactory.create(
            calendar__region=self.region,
            calendar__timeslot=self.timeslot)
        self.date = datetime.date(2012, 10, 29)

    def test_get_free_count(self):
        result = get_free_count(self.date, self.timeslot, self.region)
        self.assertEqual(3, result, "Expected 3 free places left")


class TestGetFreeEntries(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.customer = CustomerFactory.create()
        self.region = RegionFactory.create()
        self.timeslot = TimeSlotFactory.create()
        self.region.timeslots.add(self.timeslot)
        self.date = datetime.date(2012, 10, 29)
        self.appointment = AppointmentFactory.create(calendar__region=self.region,
                                                     calendar__timeslot=self.timeslot)

    def test_get_free_entries(self):
        result = get_free_entries(self.date, 21, self.region)
        self.assertEqual(3, len(result))

    def test_get_free_entries_two_weeks(self):
        result = get_free_entries(self.date, 14, self.region)
        self.assertEqual(2, len(result))


class TestIsoDate(TestCase):

    def test_from_iso_date(self):
        self.assertEqual(datetime.date(2012, 10, 2), get_date_from_iso('20121002'))


class CalendarNoDoublesTest(TestCase):
    
    def test_no_doubles(self):
        region = RegionFactory.create()
        timeslot = TimeSlotFactory.create()
        cal = CalendarFactory.create(region=region, timeslot=timeslot)
        self.assertRaises(Exception, lambda: CalendarFactory.create(region=region, timeslot=timeslot))
        assert len(Calendar.objects.all()) == 1
