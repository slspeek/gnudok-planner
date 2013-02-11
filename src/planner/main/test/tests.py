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
from django.test.client import Client
import logging
from django.core.urlresolvers import reverse


@attr('functional', 'cancel')
class CancelAppointmentTest(TestCase):
    """ tests view.create_appointment """
        
    def setUp(self):
        """ sets up a Django test client """
        self.client = Client()
        self.region = RegionFactory(name='Zuid-Oost', description='Zuid-Oost') 
        self.timeslot = TimeSlotFactory(day_of_week=5, begin=9.0, end=12.5)
        self.car = CarFactory(name='Zeeburg')
        self.rule = RuleFactory(timeslot=self.timeslot, car=self.car, region=self.region)
        self.date = datetime.date(year=2012, month=04, day=01) 
        self.calendar = CalendarFactory(date=self.date, car=self.car, timeslot=self.timeslot)
        self.customer = CustomerFactory(name='Alan Turing',
                                        postcode='1051XB',
                                        number=42,
                                        address='Town street',
                                        town='London',
                                        phone='06-12345678')
        self.appointment = AppointmentFactory(calendar=self.calendar,
                                              customer=self.customer,
                                              stuff='Machines')
        createTestUsers(self)
        
    def tearDown(self):
        User.objects.all().delete()

    @attr('fullsubmit')
    def test_cancel_appointment(self):
        """ Cancel an appointment """
        self.assertEquals(1, len(Calendar.objects.all()))
        self.assertEquals(1, len(Appointment.objects.all()))
        self.assertEquals(1, len(Customer.objects.all()))
        self.client.login(username='steven', password='jansteven')
        response = self.client.get(reverse('CancelAppointment', args=[self.appointment.pk,]),
                                    {}, follow=True)
        assert response.status_code == 200
        assert 'Alan Turing' in response.content
        response = self.client.post("/main/app/cancel/%d" % (self.appointment.pk),
                                    follow=True)
        assert response.status_code == 200
        appointment = Appointment.objects.get(pk=self.appointment.pk)
        logging.error(appointment.status)
        self.assertEquals(2, appointment.status)
        assert not Appointment.actives.exists()
        
    def test_cancel_appointment_in_calendar(self):
        self.assertEquals(len(self.calendar.active_appointments().all()), 1)
        self.appointment.status = Appointment.CANCELLED
        self.appointment.save()
        self.assertEquals(len(self.calendar.active_appointments().all()), 0)
        
        
        
    
@attr('functional')
class GetOrCreateCalendar(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.timeslot = TimeSlotFactory()
        self.region = RegionFactory()
        self.car = CarFactory()
        self.rule = RuleFactory(car=self.car, region=self.region, timeslot=self.timeslot)
        self.date = datetime.date(2012, 10, 29)
        self.calendar = CalendarFactory(date=self.date, car=self.car, timeslot=self.timeslot)

    def test_one_filled(self):
        result = get_or_create_calendar(self.timeslot.pk, self.car.pk, self.date)
        self.assertEqual(1, len(Calendar.objects.all()))
        assert result == self.calendar
        
        
@attr('functional')       
class TestRulesForRegion(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.timeslot = TimeSlotFactory()
        self.region = RegionFactory()
        self.car = CarFactory()
        self.rule = RuleFactory(car=self.car, region=self.region, timeslot=self.timeslot)

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
            CalendarFactory.create(timeslot=rule.timeslot, car=rule.car)
        create_calendar()
        self.assertRaises(Exception, create_calendar)
        assert len(Calendar.objects.all()) == 1
