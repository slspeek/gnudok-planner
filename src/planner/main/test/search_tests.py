from __future__ import absolute_import
from nose.plugins.attrib import attr
from django_webtest import WebTest
import logging
from planner.main.test.tests import RegionFactory, TimeSlotFactory, CarFactory, RuleFactory, CalendarFactory
import datetime
from .__init__ import createTestUsers, createRegion, adaMakesAppointment