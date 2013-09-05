from __future__ import absolute_import
from django.test import LiveServerTestCase

from selenium.webdriver.support.ui import Select
from django.core.urlresolvers import reverse


import time
import logging
import datetime
from .__init__ import RegionFactory, TimeSlotFactory, CarFactory, RuleFactory, CalendarFactory
from .__init__ import CustomerFactory, AppointmentFactory

from nose.plugins.attrib import attr
from .__init__ import createRootUser, createTestUsers, createRegion, createRegionEast, createTestPostcodes, adaMakesAppointment, adaMakesBigAppointment
from planner.main.models import Customer, Calendar
from planner.nlpostalcode.models import Source, Country, Province, City, Cityname, Postcode, Street
from planner.main.viewers_views import calendar_search_view
from planner.testutil.tests import DjangoSeleniumTest

VRIJDAG_11JAN = "11 Jan : Vrijdag :  13:00 - 16:30 - Auto Zeeburg"
OPHAALDAG = 'Ophaal lijst per dag'
VRIJDAG_04JAN = "04 Jan : Vrijdag : 9:00 - 12:30 - Auto Zeeburg"
DO_24JAN = "24 Jan : Donderdag : 9:00 - 12:30 - Auto Zeeburg"

ZUID_OOST = "Zuid-Oost: Zuid-Oost"


@attr('selenium', 'search') 
class SearchTest(DjangoSeleniumTest):

    def setUp(self):
        super(SearchTest, self).setUp()
        createRegion(self)
        createTestPostcodes()
        createTestUsers(self)
        adaMakesAppointment(self)
    
    def test_search_ada(self):
        """ Searches one appointment."""
        driver = self.driver
        self.login("alien", "jansteven")
        self.go_to_view(calendar_search_view, kwargs={'date_iso':'20130102'})
        self.sleep()    
        self.sleep()        
        self.set_text_field('id_name', "lovelac")
        driver.find_element_by_css_selector("button.btn").click()
        self.sleep()
        self.sleep()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Virtual Machines")
        self.assertBobyContains("4 januari")    
    
            
@attr('hook') 
class TestPreCommitHook(DjangoSeleniumTest):
    def setUp(self):
        super(TestPreCommitHook, self).setUp()
        createRegion(self)
        createTestPostcodes()
        createTestUsers(self)
    
    def test_create_two_appointment_at_same_time(self):
        """ Create two appointments at the same time """
        self.login('steven', 'jansteven')
        self.go_to_view('AppointmentEditExtra', args=['create', 'create', 20130101, ])
        self.sleep()
        self.set_text_field('id_postcode', '1102AB')
        self.set_text_field('id_name', 'Ada Lovelace')
        self.set_text_field('id_number', "25")
        self.set_text_field('id_additions', "sous")
        self.set_text_field('id_phone', '020-7123456')
        self.set_text_field('id_stuff', "Bed, boeken en servies")
        self.set_text_field('id_notes', "Lift aanwezig")
        self.set_select_field('id_weight', 'Een dagdeel')
        self.sleep()
        self.sleep()
        self.set_select_field('id_free_space', VRIJDAG_04JAN)
        #self.clickPrimairyButton()
         #Appointment has been saved
        self.date = datetime.date(year=2013, month=01, day=04)
        self.calendar = Calendar.objects.get(date=self.date, car=self.car, timeslot=self.timeslot)
        self.customer = CustomerFactory(name='Ada Lovelace', postcode='1102AB',
                                        number=42,
                                        address='Bijlmerdreef',
                                        town='Amsterdam',
                                        phone='06-12345678')
        self.appointment = AppointmentFactory(calendar=self.calendar,
                                              created=datetime.date(year=2012, month=12, day=20),
                                              customer=self.customer,
                                              employee=self.user_steven,
                                              stuff='Gehele nalatenschap',
                                              weight=4,
                                              notes='Lift aanwezig')
        self.clickPrimairyButton()
        self.sleep()
        self.assertBobyContains("Geen ruimte meer over")
              
  
VR_11JAN = "11 Jan : Vrijdag : 9:00 - 12:30 - Auto Zeeburg"

@attr('selenium', 'viewers')
class ViewersTestCase(DjangoSeleniumTest):
    """ Planner selenium test """

    def setUp(self):
        super(ViewersTestCase, self).setUp()
        createRegion(self)
        createTestPostcodes()
        createTestUsers(self)
        adaMakesAppointment(self)
        
  
    def test_view_one_appointment(self):
        """ Makes one appointment and verifies it be viewing the list as Viewer."""
        driver = self.driver
        self.login("alien", "jansteven")
        self.go_to_view('WeekView', args=[1, 0, 20130101])
        self.sleep()
        driver.find_element_by_link_text("Vrijdag 4 jan").click()
        self.sleep()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Virtual Machines")
        self.assertBobyContains("Lift aanwezig")
        self.assertBobyContains("4 januari")
            
@attr('selenium', 'new_edit')
class AppointmentEditExtra(DjangoSeleniumTest):
    """ Appointment create and edit test """
    
    def setUp(self):
        super(AppointmentEditExtra, self).setUp()
        createRegion(self)
        createTestPostcodes()
        createTestUsers(self)
    
        
    def test_create_one_appointment(self):
        """ Makes one appointment """
        self.login('steven', 'jansteven')
        self.go_to_view('AppointmentEditExtra', args=['create', 'create', 20130101, ])

        self.set_text_field('id_postcode', '1102AB')
        self.set_text_field('id_name', 'Ada Lovelace')
        self.set_text_field('id_number', "144")
        self.set_text_field('id_additions', "sous")
        self.set_text_field('id_phone', '020-7123456')
        self.set_text_field('id_stuff', "Bed, boeken en servies")
        self.set_text_field('id_notes', "Lift aanwezig")
        self.sleep()
        self.sleep()
        self.set_select_field('id_free_space', VRIJDAG_04JAN)
        self.clickPrimairyButton()
        # Appointment has been saved
        self.sleep()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Bed, boeken en servies")
        self.assertBobyContains("4 januari")
            
    def test_edit_appointment(self):
        """ Edit appointments stuff"""
        adaMakesAppointment(self)
        self.login('steven', 'jansteven')
        
        self.go_to_view('AppointmentEditExtra', args=[1, 1, 20130101, ])

        self.set_text_field('id_stuff', "Aantekeningen")
        self.set_text_field('id_notes', "Eerste programmeur")
        self.sleep()
        self.clickPrimairyButton()
        # Appointment has been saved
        self.sleep()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Aantekeningen")
        self.assertBobyContains("4 januari")
    
    @attr('past')
    def test_edit_appointment_from_the_past(self):
        """ Edit appointments stuff from the past"""
        adaMakesAppointment(self)
        self.appointment.calendar.date = datetime.date(2012, 12, 12)
        self.appointment.calendar.save()
        self.login('steven', 'jansteven')
        
        self.go_to_view('AppointmentEditExtra', args=[1, 1, 20130101, ])

        self.set_text_field('id_stuff', "Aantekeningen")
        self.set_text_field('id_notes', "Eerste programmeur")
        self.sleep()
        self.clickPrimairyButton()
        # Appointment has been saved
        self.sleep()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Aantekeningen")
        self.assertBobyContains("12 december")
        
    def test_edit_appointment_in_full_timeslot(self):
        """ Edit appointments stuff, in full timeslot"""
        adaMakesBigAppointment(self)
        self.login('steven', 'jansteven')
        
        self.go_to_view('AppointmentEditExtra', args=[1, 1, 20130101, ])

        self.set_text_field('id_stuff', "Aantekeningen")
        self.set_text_field('id_notes', "Eerste programmeur")
        self.sleep()
        self.clickPrimairyButton()
        # Appointment has been saved
        self.sleep()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Aantekeningen")
        self.assertBobyContains("4 januari")
    
    def test_create_follow_up(self):
        """ Create follow up """
        adaMakesAppointment(self)
        self.login('steven', 'jansteven')
        
        self.go_to_view('AppointmentEditExtra', args=['create', 1, 20130101, ])

        self.set_text_field('id_stuff', "Oude wiskunde boeken")
        self.set_text_field('id_notes', "Er een programmeertaal naar haar genoemd")
        #self.sleep()
        #self.sleep()
        self.set_select_field('id_free_space', VR_11JAN)
        self.clickPrimairyButton()
        # Appointment has been saved
        self.sleep()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Oude wiskunde boeken")
        self.assertBobyContains("11 januari")

    @attr('right_now')
    def test_existing_cutomer(self):
        """ Creating with existing cutomer """
        adaMakesAppointment(self)
        self.appointment.delete()
        assert Customer.objects.all().exists()
        self.login('steven', 'jansteven')
        
        self.go_to_view('AppointmentEditExtra', args=['create', 'create', 20130101, ])
        
        self.set_text_field('id_postcode', '1102AB')
        self.sleep()
        self.set_text_field('id_number', "42")
        self.sleep()
        self.set_text_field('id_additions', "")
        self.sleep()
        self.set_text_field('id_stuff', "Oude wiskunde boeken")
        self.set_select_field('id_free_space', VR_11JAN)
        self.clickPrimairyButton()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Oude wiskunde boeken")
        self.assertBobyContains("11 januari")

    @attr('at_first')
    def test_existing_cutomer_at_first(self):
        """ Look like an exiting customer, and then change again to new customer """
        adaMakesAppointment(self)
        self.appointment.delete()
        assert Customer.objects.all().exists()
        self.login('steven', 'jansteven')
        logging.error(Customer.objects.all())
        self.go_to_view('AppointmentEditExtra', args=['create', 'create', 20130101, ])

        self.set_text_field('id_postcode', '1102AB')
        self.set_text_field('id_number', "42")
        self.set_text_field('id_additions', "")
        self.sleep()
        self.set_text_field('id_number', "43")
        self.set_text_field('id_stuff', "Oude wiskunde boeken")
        self.set_text_field('id_notes', "Er een programmeertaal naar haar genoemd")
        #self.sleep()
        #self.sleep()
        self.set_select_field('id_free_space', VR_11JAN)
        self.clickPrimairyButton()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Oude wiskunde boeken")
        self.assertBobyContains("11 januari")
        self.assertEquals(2, len(Customer.objects.all()))
        logging.error(Customer.objects.all())
     
    @attr('no_stuff') 
    def test_create_one_appointment_without_stuff(self):
        """ Makes one appointment without stuff"""
        self.login('steven', 'jansteven')
        self.go_to_view('AppointmentEditExtra', args=['create', 'create', 20130101, ])
        
        self.set_text_field('id_postcode', '1102AB')
        self.set_text_field('id_name', 'Ada Lovelace')
        self.set_text_field('id_number', "144")
        self.set_text_field('id_additions', "sous")
        self.set_text_field('id_phone', '020-7123456')
        #self.set_text_field('id_stuff', "Bed, boeken en servies")
        self.set_text_field('id_notes', "Lift aanwezig")
        self.sleep()
        self.sleep()
        self.set_select_field('id_free_space', VRIJDAG_04JAN)
        self.clickPrimairyButton()
        # Appointment has been saved
        self.sleep()
        
        self.assertBobyContains("Dit veld is verplicht")
           
    @attr('unres')
    def test_unrestricted(self):
        """ Create unrestricted appointment """
        self.login('steven', 'jansteven')
        
        self.go_to_view('AppointmentEditExtra', args=['create', 'create', 20130101, ])
        self.driver.find_element_by_id("id_unrestricted").click()
        self.sleep()
        self.sleep()
        self.set_text_field('id_postcode', '1000AA')
        self.set_text_field('id_number', "42")
        self.set_text_field('id_address', "Town street")
        self.set_text_field('id_town', "London")
        self.set_text_field('id_name', 'Ada Lovelace')
        self.set_text_field('id_stuff', "Oude wiskunde boeken")
        self.set_text_field('id_phone', '020-7123456')
        self.sleep()
        self.set_select_field('id_free_space', VR_11JAN)
        self.clickPrimairyButton()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Oude wiskunde boeken")
        self.assertBobyContains("11 januari")
        self.assertBobyContains("London")
        
@attr('selenium', 'multiple')
class AppointmentEditMultipleRegions(DjangoSeleniumTest):
    """ Appointment create appointment with a multiple region postcode """
    
    def setUp(self):
        super(AppointmentEditMultipleRegions, self).setUp()
        createRegion(self)
        createRegionEast(self)
        createTestPostcodes()
        createTestUsers(self)
        
        
    def test_create_one_appointment_in_east(self):
        """ Makes one appointment in east"""
        self.login('steven', 'jansteven')
        self.go_to_view('AppointmentEditExtra', args=['create', 'create', 20130101, ])

        self.set_text_field('id_postcode', '1102AB')
        self.set_text_field('id_name', 'Ada Lovelace')
        self.set_text_field('id_number', "144")
        self.set_text_field('id_additions', "sous")
        self.set_text_field('id_phone', '020-7123456')
        self.set_text_field('id_stuff', "Bed, boeken en servies")
        self.set_text_field('id_notes', "Lift aanwezig")
        self.sleep()
        self.sleep()
        self.set_select_field('id_free_space', DO_24JAN)
        self.clickPrimairyButton()
        # Appointment has been saved
        self.sleep()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Bed, boeken en servies")
        self.assertBobyContains("24 januari")

        
