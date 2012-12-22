'''
Test for the function that saves the Customer, Appointment and Calendar objects.
'''
from __future__ import absolute_import
from nose.plugins.attrib import attr
from django_webtest import WebTest
import logging
from planner.main.test.tests import RegionFactory, TimeSlotFactory, CarFactory, RuleFactory, CalendarFactory
import datetime
from .__init__ import createTestUsers, createRegion, adaMakesAppointment
from django.core.urlresolvers import reverse
from planner.main.viewers_views import appointment_detail
from django.test.testcases import TestCase
from planner.main.models import Appointment

@attr('functional', 'webtest')
class AppointmentDetail(WebTest):
    
    def setUp(self):
        super(AppointmentDetail, self).setUp()
        createRegion(self)
        createTestUsers(self)
        adaMakesAppointment(self)
         
    def testAppointmentDetail(self):
        """ Verifies the presence of all appoinment details in the page """
        login = self.app.get(reverse(appointment_detail, args=[self.appointment.pk,])).follow()
        login_form = login.form
        login_form['username'] = 'steven'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        details = redirect.follow()
        assert "Ada Lovelace" in details
        assert "Lift aanwezig" in details
        assert "Virtual Machines" in details
      
@attr('functional', 'webtest')
class AppointmentsByDate(WebTest):
    
    def setUp(self):
        super(AppointmentsByDate, self).setUp()
        createRegion(self)
        createTestUsers(self)
        adaMakesAppointment(self)
    
    @attr('today')
    def testAppointmentsToday(self):
        """ Verifies that if no arguments given today is assumed """
        self.appointment.created = datetime.date.today()
        self.appointment.save()
        login = self.app.get(reverse('AppointmentsToday', args=['',])).follow()
        login_form = login.form
        login_form['username'] = 'alien'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        details = redirect.follow()
        assert "Ada Lovelace" in details
        assert "Lift aanwezig" in details
        assert "Virtual Machines" in details
         
    def testAppointmentsByDate(self):
        """ Verifies the presence of an appoinment by date """
        login = self.app.get(reverse('AppointmentsToday', args=[20121220,])).follow()
        login_form = login.form
        login_form['username'] = 'alien'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        details = redirect.follow()
        assert "Ada Lovelace" in details
        assert "Lift aanwezig" in details
        assert "Virtual Machines" in details

    def testCancelledInvisible(self):
        """ Verifies the absence of a cancelled appoinment in the by date view """
        self.appointment.status = Appointment.CANCELLED
        self.appointment.save()
    
        login = self.app.get(reverse('AppointmentsToday', args=[20121220,])).follow()
        login_form = login.form
        login_form['username'] = 'alien'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        details = redirect.follow()
        assert not "Ada Lovelace" in details
        assert not "Virtual Machines" in details
        
          
@attr('functional', 'webtest')
class AppointmentsByEmployee(WebTest):
    
    def setUp(self):
        super(AppointmentsByEmployee, self).setUp()
        createRegion(self)
        createTestUsers(self)
        adaMakesAppointment(self)
         
    def testAppointmentsByDate(self):
        """ Verifies the presence of an appoinment by employee """
        login = self.app.get(reverse('AppointmentsMadeBy', args=[self.user_steven.pk,])).follow()
        login_form = login.form
        login_form['username'] = 'alien'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        details = redirect.follow()
        assert "Ada Lovelace" in details
        assert "Virtual Machines" in details

    def testCancelledInvisible(self):
        """ Verifies the absence of a cancelled appoinment in the by employee view """
        self.appointment.status = Appointment.CANCELLED
        self.appointment.save()
    
        login = self.app.get(reverse('AppointmentsMadeBy', args=[self.user_steven.pk,])).follow()
        login_form = login.form
        login_form['username'] = 'alien'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        details = redirect.follow()
        assert not "Ada Lovelace" in details
        assert not "Virtual Machines" in details
    
    @attr('special')
    def testChooseEmployee(self):
        """ Checks that steven is selectable """
        login = self.app.get(reverse('ChooseAnEmployee')).follow()
        login_form = login.form
        login_form['username'] = 'alien'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        choose_an_employee = redirect.follow()
        form = choose_an_employee.form
        print choose_an_employee, form.fields.values()
        form['employee'] = u'1'
        details = form.submit().follow()
        assert "Ada Lovelace" in details
        assert "Virtual Machines" in details
        
@attr('functional', 'weekview')
class Weekview(WebTest):
    
    def setUp(self):
        super(Weekview, self).setUp()
        createRegion(self)
        createTestUsers(self)
        adaMakesAppointment(self)
         
    def testWeekview(self):
        """ Verifies the presence of an appoinment in the weekview """
        login = self.app.get(reverse('WeekView', args=[self.car.pk,0,20130104])).follow()
        login_form = login.form
        login_form['username'] = 'alien'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        details = redirect.follow()
        assert "Ada Lovelace" in details
        

    def testCancelledInvisible(self):
        """ Verifies the absence of a cancelled appoinment in the by employee view """
        self.appointment.status = Appointment.CANCELLED
        self.appointment.save()
    
        login = self.app.get(reverse('WeekView', args=[self.car.pk,0,20130104])).follow()
        login_form = login.form
        login_form['username'] = 'alien'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        details = redirect.follow()
        assert not "Ada Lovelace" in details
        
    
        

