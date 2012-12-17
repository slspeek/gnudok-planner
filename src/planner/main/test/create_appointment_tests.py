'''
Test for the function that saves the Customer, Appointment and Calendar objects.
'''
from __future__ import absolute_import
from django.test.client import Client

from planner.main.models import Calendar, Appointment, Customer
from django.test.testcases import TestCase
import datetime
from planner.main.test.tests import RegionFactory, TimeSlotFactory, CarFactory, RuleFactory, CalendarFactory
from nose.plugins.attrib import attr
from .__init__ import createTestUsers

@attr('functional')
class CreateAppointmentTest(TestCase):
    """ tests view.create_appointment """
    
    def setUp(self):
        """ sets up a Django test client """
        self.client = Client()
        self.region = RegionFactory(name='Zuid-Oost', description='Zuid-Oost') 
        self.timeslot = TimeSlotFactory(day_of_week=5,begin=9.0,end=12.5)
        self.car = CarFactory(name='Zeeburg')
        self.rule = RuleFactory(timeslot=self.timeslot, car=self.car, region=self.region)
        self.date = datetime.date(year=2012,month=04,day=01) 
        self.calendar = CalendarFactory(date=self.date, car=self.car, timeslot=self.timeslot)
        createTestUsers(self)
        
    @attr('fullsubmit')
    def testFullSubmit(self):
        """ tests a successfull submit """
        assert len(Calendar.objects.all()) == 1
        assert len(Appointment.objects.all()) == 0
        assert len(Customer.objects.all()) == 0
        self.client.login(username='steven', password='jansteven')
        response = self.client.post("/main/app/create/%s/%d" % (self.calendar.pk, 1),
                                    {'name': 'Alan Turing',
                                     'postcode': '1051XB',
                                     'number': 42,
                                     'address': 'Townstreet 123',
                                     'town': 'London',
                                     'phone': '06-12345678',
                                     'stuff': 'Machines',
                                     'weight': 1,
                                     'calendar_id': self.calendar.pk 
                                     }, follow=True)
        assert response.status_code == 200
        assert 'Alan Turing' in response.content
        assert Customer.objects.get(pk=1).name == 'Alan Turing'
        assert Calendar.objects.get(pk=1).date.strftime('%Y%m%d') == '20120401'
        assert Appointment.objects.get(pk=1).stuff == 'Machines'
    
    def testInvalidCustomer(self):
        """ tests a submit with invalid customer """
        assert len(Calendar.objects.all()) == 1
        assert len(Appointment.objects.all()) == 0
        assert len(Customer.objects.all()) == 0
        self.client.login(username='steven', password='jansteven')
        response = self.client.post("/main/app/create/%s/%d" % (self.calendar.pk, 1),
                                    {
                                     'postcode': '1051XB',
                                     'number': 42,
                                     'address': 'Townstreet 123',
                                     'town': 'London',
                                     'phone': '06-12345678',
                                     'stuff': 'Machines',
                                     'weight': 1,
                                     'calendar_id': self.calendar.pk 
                                    
                                     }, follow=True)
        assert response.status_code == 200
        assert 'Dit veld is verplicht.' in response.content
        assert len(Calendar.objects.all()) == 1
        assert len(Appointment.objects.all()) == 0
        assert len(Customer.objects.all()) == 0
    
    def testTwoAppointmentsOnSameTimeslot(self):
        """ tests submitting two appointments, and assert we have one calendar at the
        end """
        assert len(Calendar.objects.all()) == 1
        assert len(Appointment.objects.all()) == 0
        assert len(Customer.objects.all()) == 0
        self.client.login(username='steven', password='jansteven')
        response = self.client.post("/main/app/create/%s/%d" % (self.calendar.pk, 1),
                                    {'name': 'Alan Turing',
                                     'postcode': '1051XB',
                                     'number': 42,
                                     'address': 'Townstreet 123',
                                     'town': 'London',
                                     'phone': '06-12345678',
                                     'stuff': 'Machines',
                                     'weight': 1,
                                     'calendar_id': self.calendar.pk  
                                     }, follow=True)
        assert response.status_code == 200
        assert 'Alan Turing' in response.content
        assert Customer.objects.get(pk=1).name == 'Alan Turing'
        assert Calendar.objects.get(pk=1).date.strftime('%Y%m%d') == '20120401'
        assert Appointment.objects.get(pk=1).stuff == 'Machines'
        response = self.client.post("/main/app/create/%s/%d" % (self.calendar.pk, 1),
                                    {'name': 'Godel',
                                     'postcode': '1011XB',
                                     'number': 41,
                                     'address': 'Townstreet 121',
                                     'town': 'London',
                                     'phone': '06-12345678',
                                     'stuff': 'Machines',
                                     'weight': 1,
                                     'calendar_id': self.calendar.pk  
                                     }, follow=True)
        assert response.status_code == 200
        assert 'Godel' in response.content
        assert Customer.objects.get(pk=2).name == 'Godel'
        assert len(Calendar.objects.all()) == 1
        assert len(Customer.objects.all()) == 2
        assert len(Appointment.objects.all()) == 2
        
            
    def testNoStuff(self):
        """ tests a lacking stuff and assert the database does not change """ 
        assert len(Calendar.objects.all()) == 1
        assert len(Appointment.objects.all()) == 0
        assert len(Customer.objects.all()) == 0
        self.client.login(username='steven', password='jansteven')
        response = self.client.post("/main/app/create/%s/%d" % (self.calendar.pk, 1),
                                    {'name': 'Alan Turing',
                                     'postcode': '1051XB',
                                     'number': 42,
                                     'address': 'Townstreet 123',
                                     'town': 'London',
                                     'phone': '06-12345678',
                                     'weight': 1,
                                     'calendar_id': self.calendar.pk  
                                     }, follow=True)
        assert response.status_code == 200
        assert 'Dit veld is verplicht.' in response.content
        assert len(Calendar.objects.all()) == 1
        assert len(Appointment.objects.all()) == 0
        assert len(Customer.objects.all()) == 0