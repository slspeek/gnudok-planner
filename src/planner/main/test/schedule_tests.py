'''
Created on 29 nov. 2012

@author: steven
'''
from __future__ import absolute_import
import datetime
from planner.main.schedule import _get_rules, get_free_count, get_free_entries_new, APPOINTMENTS_PER_HALF_DAY
from django.test.testcases import TestCase
from planner.main.test.tests import RuleFactory, CarFactory, TimeSlotFactory, AppointmentFactory
from nose.plugins.attrib import attr
from planner.main.test import RegionFactory

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
        assert _get_rules(self.date, self.region)
    
    def testNoRules(self):
        assert not _get_rules(self.other_date, self.region)
    
    def testUnrestrictedRules(self):
        assert _get_rules(self.date, None)
        
@attr('functional')
class TestNoAppointmentsOnCalendar(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.rule = RuleFactory()

    def test_get_free_count(self):
        date = datetime.date(2012, 10, 29)
        result = get_free_count(date, self.rule)
        self.assertEqual(APPOINTMENTS_PER_HALF_DAY, result, "Expected %s free places" % APPOINTMENTS_PER_HALF_DAY)
        
    def test_settings(self):
        import planner.settings as s
        print s.MEDIA_ROOT

@attr('functional')
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
        self.assertEqual(APPOINTMENTS_PER_HALF_DAY - 1, result, "Expected 3 free places left")

@attr('functional', 'cancelled')
class TestCancelledAppointmentsDoNotCount(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.car = CarFactory()
        self.timeslot = TimeSlotFactory()
        self.rule = RuleFactory(car=self.car, timeslot=self.timeslot)
        self.appointment = AppointmentFactory.create(
            calendar__car=self.car,
            calendar__timeslot=self.timeslot)
        self.appointment.status = 2
        self.date = datetime.date(2012, 10, 29)
        self.appointment.save()

    def test_get_free_count(self):
        result = get_free_count(self.date, self.rule)
        self.assertEqual(APPOINTMENTS_PER_HALF_DAY, result, "Expected 4 free places left, cancelled should not count")


@attr('functional', 'getfreeentries')
class TestGetFreeEntries(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.rule = RuleFactory()
        self.date = datetime.date(2012, 10, 29)
        self.appointment = AppointmentFactory.create(calendar__car=self.rule.car,
                                                     calendar__timeslot=self.rule.timeslot)

    def test_get_free_entries(self):
        result = get_free_entries_new(self.date, 21, [self.rule.region], 1)
        self.assertEqual(3, len(result))

    def test_get_free_entries_new_two_weeks(self):
        result = get_free_entries_new(self.date, 14, [self.rule.region], 1)
        self.assertEqual(2, len(result))
        
        
@attr('functional')
class TestGetFreeEntriesWithHeavyWeight(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.rule = RuleFactory()
        self.date = datetime.date(2012, 10, 29)

    def test_get_free_entries(self):
        result = get_free_entries_new(self.date, 21, [self.rule.region], 1)
        self.assertEqual(3, len(result))

    def test_get_free_entries_two_weeks(self):
        result = get_free_entries_new(self.date, 14, [self.rule.region], 1)
        self.assertEqual(2, len(result))

