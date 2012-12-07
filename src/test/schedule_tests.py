'''
Created on 29 nov. 2012

@author: steven
'''
from __future__ import absolute_import
from planner.main.schedule import *
from django.test.testcases import TestCase
from planner.main.tests import RuleFactory, CarFactory, TimeSlotFactory, AppointmentFactory
from nose.plugins.attrib import attr

@attr('functional')
class TestNoAppointmentsOnCalendar(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.rule = RuleFactory()

    def test_get_free_count(self):
        date = datetime.date(2012, 10, 29)
        result = get_free_count(date, self.rule)
        self.assertEqual(4, result, "Expected 4 free places")

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
        self.assertEqual(3, result, "Expected 3 free places left")


@attr('functional')
class TestGetFreeEntries(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.rule = RuleFactory()
        self.date = datetime.date(2012, 10, 29)
        self.appointment = AppointmentFactory.create(calendar__car=self.rule.car,
                                                     calendar__timeslot=self.rule.timeslot)

    def test_get_free_entries(self):
        result = get_free_entries(self.date, 21, self.rule.region, 1)
        self.assertEqual(3, len(result))

    def test_get_free_entries_two_weeks(self):
        result = get_free_entries(self.date, 14, self.rule.region, 1)
        self.assertEqual(2, len(result))
        
        
@attr('functional')
class TestGetFreeEntriesWithHeavyWeight(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.rule = RuleFactory()
        self.date = datetime.date(2012, 10, 29)
        self.appointment = AppointmentFactory.create(calendar__car=self.rule.car,weight=4,
                                                     calendar__timeslot=self.rule.timeslot)

    def test_get_free_entries(self):
        result = get_free_entries(self.date, 21, self.rule.region, 1)
        self.assertEqual(2, len(result))

    def test_get_free_entries_two_weeks(self):
        result = get_free_entries(self.date, 14, self.rule.region, 1)
        self.assertEqual(2, len(result))

