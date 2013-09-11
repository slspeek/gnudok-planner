'''
Created on 29 nov. 2012

@author: steven
'''
from __future__ import absolute_import
import datetime
from planner.main.schedule import _get_rules, get_free_count, get_free_entries, get_limit
from django.test.testcases import TestCase
from planner.main.test.tests import RuleFactory, CarFactory, TimeSlotFactory, AppointmentFactory
from nose.plugins.attrib import attr
from planner.main.test import RegionFactory
from planner.main.models import Appointment

@attr('functional', 'get_rules')
class GetRules(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
        self.car = CarFactory()
        self.region = RegionFactory()
        self.timeslot = TimeSlotFactory()
        self.rule = RuleFactory(car=self.car, timeslot=self.timeslot, region=self.region)
        self.appointment = AppointmentFactory.create(
            calendar__car=self.car,
            calendar__timeslot=self.timeslot)
        self.date = datetime.date(2012, 10, 29)
        self.other_date = datetime.date(2012, 10, 30)

    def testRules(self):
        assert _get_rules(self.date, self.region, None)
    
    def testNoRules(self):
        assert not _get_rules(self.other_date, self.region, None)
    
    def testUnrestrictedRules(self):
        assert _get_rules(self.date, None, None)
        
@attr('functional', 'test_now')
class TestNoAppointmentsOnCalendar(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.rule = RuleFactory()
        

    def test_get_free_count_for_delivery(self):
        """ No delivery slot taken """
        date = datetime.date(2012, 10, 29)
        result = get_free_count(date, self.rule, Appointment.KIND_DELIVERY)
        expected = get_limit(Appointment.KIND_DELIVERY)
        self.assertEqual(expected, result, "Expected %s free places" % expected)
    
    def test_get_free_count_for_pickup(self):
        """ No pickup slot taken """
        date = datetime.date(2012, 10, 29)
        result = get_free_count(date, self.rule, Appointment.KIND_PICKUP)
        expected = get_limit(Appointment.KIND_PICKUP)
        self.assertEqual(expected, result, "Expected %s free places" % expected)
        
    
@attr('functional', 'test_now')
class TestAppointmentCalendarWithOneDeliveryPresent(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.car = CarFactory()
        self.timeslot = TimeSlotFactory()
        self.rule = RuleFactory(car=self.car, timeslot=self.timeslot)
        self.appointment = AppointmentFactory.create(
            calendar__car=self.car,
            calendar__timeslot=self.timeslot,
            kind=Appointment.KIND_DELIVERY,
            weight=1)
        self.date = datetime.date(2012, 10, 29)

    def test_get_free_count_for_delivery(self):
        """ One delivery slot taken """
        result = get_free_count(self.date, self.rule, Appointment.KIND_DELIVERY)
        open_delivery_places = get_limit(Appointment.KIND_DELIVERY) - 1
        self.assertEqual(open_delivery_places, result, "Expected %s free places left" % open_delivery_places)

    def test_get_free_count_for_pickup(self):
        """ No pickup slot taken """
        result = get_free_count(self.date, self.rule, Appointment.KIND_PICKUP)
        open_pickup_places = get_limit(Appointment.KIND_PICKUP)
        self.assertEqual(open_pickup_places, result, "Expected %s free places left" % open_pickup_places)

@attr('functional', 'cancelled')
class TestCancelledAppointmentsDoNotCount(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.car = CarFactory()
        self.timeslot = TimeSlotFactory()
        self.rule = RuleFactory(car=self.car, timeslot=self.timeslot)
        self.appointment = AppointmentFactory.create(
            calendar__car=self.car,
            calendar__timeslot=self.timeslot,
            kind=Appointment.KIND_PICKUP,
            weight=1)
        self.appointment.status = 2
        self.date = datetime.date(2012, 10, 29)
        self.appointment.save()

    def test_get_free_count(self):
        """ Cancelled appointments should not take up space """
        result = get_free_count(self.date, self.rule, Appointment.KIND_PICKUP)
        expected = get_limit(Appointment.KIND_PICKUP)
        self.assertEqual(expected, result, "Expected %s free places left, cancelled should not count" % expected)


@attr('functional', 'getfreeentries')
class TestGetFreeEntries(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.rule = RuleFactory()
        self.date = datetime.date(2012, 10, 29)
        self.appointment = AppointmentFactory.create(calendar__car=self.rule.car,
                                                     calendar__timeslot=self.rule.timeslot)

    def test_get_free_entries(self):
        result = get_free_entries(self.date, 21, [self.rule.region], 1, 2, None)
        self.assertEqual(3, len(result))

    def test_get_free_entries_two_weeks(self):
        result = get_free_entries(self.date, 14, [self.rule.region], 1, 2, None)
        self.assertEqual(2, len(result))
        
        
@attr('functional')
class TestGetFreeEntriesWithHeavyWeight(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.rule = RuleFactory()
        self.date = datetime.date(2012, 10, 29)

    def test_get_free_entries(self):
        result = get_free_entries(self.date, 21, [self.rule.region], 1, 2, None)
        self.assertEqual(3, len(result))

    def test_get_free_entries_two_weeks(self):
        result = get_free_entries(self.date, 14, [self.rule.region], 1, 2, None)
        self.assertEqual(2, len(result))


