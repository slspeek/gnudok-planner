'''
Test for the function that saves the Customer, Appointment and Calendar objects.
'''
from __future__ import absolute_import
from nose.plugins.attrib import attr
from django_webtest import WebTest
import logging
from planner.main.test.tests import RegionFactory, TimeSlotFactory, CarFactory, RuleFactory, CalendarFactory
import datetime

@attr('functional', 'webtest')
class MyTestCase(WebTest):

    fixtures = ['test_data.json',]
    
    def setUp(self):
        self.region = RegionFactory(name='Zuid-Oost', description='Zuid-Oost') 
        self.timeslot = TimeSlotFactory(day_of_week=5,begin=9.0,end=12.5)
        self.car = CarFactory(name='Zeeburg')
        self.rule = RuleFactory(timeslot=self.timeslot, car=self.car, region=self.region)
        self.date = datetime.date(year=2012,month=04,day=01) 
        self.calendar = CalendarFactory(date=self.date, car=self.car, timeslot=self.timeslot)
         
    def testNewAppointment(self):
        login = self.app.get('/main/edit/create/create').follow().follow()
        
        login_form = login.form
        login_form['username'] = 'steven'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        index = redirect.follow()
        
        self.assertContains(index, 'Nieuwe')
        form = index.form
        form['name'] = 'Alan Turing'
        form['postcode'] = '1051XB'
        form['number'] = 42,
        form['address'] = 'Townstreet'
        form['town'] = 'London'
        form['phone'] = '06-12345678'
        form['stuff'] = 'Machines'
        form['weight'] = 1
        #form['free_space'] = self.calendar.pk 
        #assert "Gemaakte afspraak" in form.submit()