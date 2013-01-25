from __future__ import absolute_import
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from django.core.urlresolvers import reverse


import time
import datetime
from .__init__ import RegionFactory, TimeSlotFactory, CarFactory, RuleFactory, CalendarFactory
from .__init__ import CustomerFactory, AppointmentFactory
import os
from nose.plugins.attrib import attr
from .__init__ import createTestUsers, createRegion, createTestPostcodes, adaMakesAppointment, adaMakesBigAppointment
from planner.main.models import Customer, Calendar

VRIJDAG_11JAN = "11 January : Vrijdag :  13:00 - 16:30 - Auto Zeeburg"
OPHAALDAG = 'Ophaal lijst per dag'
VRIJDAG_04JAN = "04 January : Vrijdag : 9:00 - 12:30 - Auto Zeeburg"

ZUID_OOST = "Zuid-Oost: Zuid-Oost"

class DjangoSeleniumTest(LiveServerTestCase):
    """ Base class for the django selenium testing """

    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        super(DjangoSeleniumTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(DjangoSeleniumTest, cls).tearDownClass()
        cls.driver.quit()
        
    def sleep(self):
        amount = float(os.environ.get("TEST_PAUSE", failobj=2))
        time.sleep(amount)

    def set_text_field(self, field_id, value):
        self.driver.find_element_by_id(field_id).clear()
        self.driver.find_element_by_id(field_id).send_keys(value)
    
    def set_select_field(self, field_id, value):
        Select(self.driver.find_element_by_id(field_id)).select_by_visible_text(value)
    
    def assertBobyContains(self, text):
        self.assertRegexpMatches(self.driver.find_element_by_css_selector("BODY").text, text)
    
    def clickPrimairyButton(self):
        self.driver.find_element_by_css_selector("button.btn.btn-primary").click()
        self.sleep()
    
    def logout(self):
        self.driver.get(self.live_server_url + reverse('Logout'))
        self.sleep()
        
    def login(self, username, password):
        #self.driver.get(self.live_server_url + "/accounts/login/?next=" + next)
        self.go_to_view('Login')
        self.sleep()
        self.set_text_field('id_username', username)
        self.set_text_field('id_password', password)
        self.driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.sleep()
    
    def go_to_view(self, view, args=None, kwargs=None):
        self.driver.get(self.live_server_url + reverse(view, args=args, kwargs=kwargs))
        
@attr('hook') 
class TestPreCommitHook(DjangoSeleniumTest):
    def setUp(self):
        createRegion(self)
        createTestPostcodes()
        createTestUsers(self)
    
    def test_create_two_appointment_at_same_time(self):
        """ Create two appointments at the same time """
        self.login('steven', 'jansteven')
        self.go_to_view('AppointmentEditExtra', args=['create', 'create', 20130101, ])

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
        self.assertBobyContains("No more space left")
              
  
VR_11JAN = "11 January : Vrijdag : 9:00 - 12:30 - Auto Zeeburg"

@attr('selenium', 'viewers')
class ViewersTestCase(DjangoSeleniumTest):
    """ Planner selenium test """

    def setUp(self):
        createRegion(self)
        createTestPostcodes()
        createTestUsers(self)
        adaMakesAppointment(self)
    
    def test_view_one_appointment(self):
        """ Makes one appointment and verifies it be viewing the list as Viewer."""
        driver = self.driver
        self.login("alien", "jansteven")
        self.go_to_view('WeekView', args=[1, 0, 20130101])
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

    
    def test_existing_cutomer_at_first(self):
        """ Look like an exiting customer, and then change again to new customer """
        adaMakesAppointment(self)
        self.appointment.delete()
        assert Customer.objects.all().exists()
        self.login('steven', 'jansteven')
        
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
        assert len(Customer.objects.all()) == 2
    
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
        
