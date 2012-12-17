from __future__ import absolute_import
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from django.core.urlresolvers import reverse


import time
from .__init__ import RegionFactory, TimeSlotFactory, CarFactory, RuleFactory
import os
from nose.plugins.attrib import attr
from .__init__ import createTestUsers, createRegion, createTestPostcodes

VRIJDAG_11JAN = "11 January : Vrijdag :  13 - 16 - Zeeburg"
OPHAALDAG = 'Ophaal lijst per dag'
VRIJDAG_04JAN = "04 January : Vrijdag : 9 - 12 - Zeeburg"
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

@attr('selenium', 'big') 
class SeleniumTestCase(DjangoSeleniumTest):
    """ Planner selenium test """
    
    
    def setUp(self):
        createRegion()
        createTestPostcodes()
        createTestUsers(self)

    @attr('make_one')
    def test_make_one_appointment(self):
        """ Makes one appointment and verifies that the details are shown in the listing for that car """
        driver = self.driver
        self.login('steven', 'jansteven')
        self.go_to_view('ChooseARegion', args=[20130101, ])
        self.set_select_field('id_region', ZUID_OOST)
        self.clickPrimairyButton()
        self.set_select_field('id_free_space', VRIJDAG_11JAN)
        self.clickPrimairyButton()
        self.set_text_field('id_name', 'Ada Lovelace')
        self.set_text_field('id_postcode', '1102AB')
        #self.set_text_field('id_address', '')
        #self.set_text_field('id_town', 'Amsterdam-Zuidoost')
        self.set_text_field('id_number', "144")
        self.set_text_field('id_additions', "sous")
        self.set_text_field('id_phone', '020-7123456')
        self.set_text_field('id_stuff', "Bed, boeken en servies")
        self.set_text_field("id_notes", "Lift aanwezig")
        self.sleep()
        self.clickPrimairyButton()
        self.assertBobyContains("Bed, boeken en servies")
        driver.find_element_by_link_text("Ophaal lijst per dag").click()
        self.sleep()
        self.set_text_field('id_date', "04-01-2013 ")
        driver.find_element_by_id("title").click()
        self.clickPrimairyButton()
        driver.find_element_by_link_text("Auto Zeeburg").click()
        self.sleep()
        self.assertBobyContains("Bed, boeken en servies")
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("1102AB")
        self.assertBobyContains("Lift aanwezig")
        self.assertBobyContains("144")
        self.assertBobyContains("sous")
        self.assertBobyContains("020-7123456")
        self.assertBobyContains("sous")
        
        
    def test_search_appointment(self):
        """ Makes one appointment and verifies that the details are the listing for the drivers """
        driver = self.driver
        self.login('steven', 'jansteven')
        self.go_to_view('ChooseARegion', args=[20130101, ])
        self.set_select_field('id_region', ZUID_OOST)
        self.clickPrimairyButton()
        self.set_select_field('id_free_space', VRIJDAG_11JAN)
        self.clickPrimairyButton()
        self.set_text_field('id_name', 'Ada Lovelace')
        self.set_text_field('id_postcode', '1102AB')
        self.set_text_field('id_address', 'Bijlmerdreef')
        self.set_text_field('id_town', 'Amsterdam-Zuidoost')
        self.set_text_field('id_number', "144")
        self.set_text_field('id_phone', '020-7123456')
        self.set_text_field('id_stuff', "Bed, boeken en servies")
        self.set_text_field("id_notes", "Lift aanwezig")
        self.clickPrimairyButton()
        self.assertBobyContains("Bed, boeken en servies")
        driver.find_element_by_link_text("Afspraak zoeken").click()
        self.sleep()        
        self.set_text_field('id_name', "lovelac")
        driver.find_element_by_css_selector("button.btn").click()
        self.sleep()
        self.assertBobyContains("Ada Lovelace")

    def test_make_four_appointments(self):
        """ Make four appointments in the same timeslot, region and date to see that that date is no longer 
            suggested """
        driver = self.driver
        self.login('steven', 'jansteven')
        self.go_to_view('ChooseARegion', args=[20130101, ])
        self.set_select_field('id_region', ZUID_OOST)
        self.clickPrimairyButton()
        self.set_select_field('id_free_space', VRIJDAG_11JAN)  
        self.clickPrimairyButton()
        self.set_text_field('id_name', 'Ada Lovelace')
        self.set_text_field('id_postcode', '1102AB')
        self.set_text_field('id_address', 'Bijlmerdreef')
        self.set_text_field('id_town', 'Amsterdam-Zuidoost')
        self.set_text_field('id_number', "144")
        self.set_text_field('id_phone', '020-7123456')
        self.set_text_field('id_stuff', "Bed, boeken en servies")
        self.set_text_field("id_notes", "Lift aanwezig")
        self.clickPrimairyButton()
        self.assertBobyContains("Bed, boeken en servies")

        self.go_to_view('ChooseARegion', args=[20130101, ])
        self.set_select_field('id_region', ZUID_OOST)
        self.clickPrimairyButton()
        self.set_select_field('id_free_space', VRIJDAG_11JAN)  
        self.clickPrimairyButton()
        self.set_text_field('id_name', "Mark de Jong")
        self.set_text_field('id_postcode', "1102AT")
        self.set_text_field('id_address', "Ken Saro-Wiwastraat")
        self.set_text_field('id_town', 'Amsterdam-Zuidoost')
        self.set_text_field('id_number', "21")
        driver.find_element_by_id("id_phone").clear()
        driver.find_element_by_id("id_phone").send_keys("020-7654321")
        self.set_text_field('id_stuff', "Speelgoed en ikea meubel")
        self.clickPrimairyButton()
        self.assertBobyContains("Speelgoed en ikea meubel")

        self.go_to_view('ChooseARegion', args=[20130101, ])
        self.set_select_field('id_region', ZUID_OOST)
        self.clickPrimairyButton()
        self.sleep()
        self.set_select_field('id_free_space', VRIJDAG_11JAN)  
        self.sleep()
        self.clickPrimairyButton()
        self.sleep()
        self.set_text_field('id_name', "Lidia van de Heuvel")
        self.set_text_field('id_postcode', "1102AX")
        self.set_text_field('id_number', "17")
        driver.find_element_by_id("id_phone").clear()
        driver.find_element_by_id("id_phone").send_keys("020-7654321")
        self.set_text_field('id_stuff', "Speelgoed, kastjes en bank")
        self.clickPrimairyButton()
        self.assertBobyContains("Speelgoed, kastjes en bank")
        
        self.go_to_view('ChooseARegion', args=[20130101, ])
        self.set_select_field('id_region', ZUID_OOST)
        self.clickPrimairyButton()
        self.set_select_field('id_free_space', VRIJDAG_11JAN)  
        self.clickPrimairyButton()
        self.set_text_field('id_name', "Mirjam de Leeuw")
        self.set_text_field('id_postcode', "1102ZA")
        self.set_text_field('id_number', "17")
        driver.find_element_by_id("id_phone").clear()
        driver.find_element_by_id("id_phone").send_keys("020-7654321")
        self.set_text_field('id_stuff', "Dozen met kleren")
        self.clickPrimairyButton()
        self.assertBobyContains("Dozen met kleren")
        
        driver.find_element_by_link_text(OPHAALDAG).click()
        self.sleep()
        self.set_text_field('id_date', "04-01-2013 ")
        driver.find_element_by_id("title").click()
        self.clickPrimairyButton()
        driver.find_element_by_link_text("Auto Zeeburg").click()
        self.sleep()
        self.assertBobyContains("Bed, boeken en servies")
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("1102AB")
        self.assertBobyContains("Lift aanwezig")
        self.assertBobyContains("144")
        self.assertBobyContains("020-7123456")
        self.go_to_view('ChooseARegion', args=[20130101, ])
        self.set_select_field('id_region', ZUID_OOST)
        self.clickPrimairyButton()
        try:
            self.assertBobyContains("11 January Friday : 9 - 12")
            raise Exception()
        except  Exception:
            pass
        driver.find_element_by_link_text("Overzicht").click()
        self.sleep()
        self.go_to_view('WeekView', args=[1, 0, 20130101])
        self.assertBobyContains("1102AB")
        self.assertBobyContains("Ada Lovelace")
        
 
VR_11JAN = "11 January : Vrijdag : 9 - 12 - Auto Zeeburg"
   
@attr('selenium', 'edit')
class EditTestCase(DjangoSeleniumTest):
    """ Planner selenium test """
    
    def setUp(self):
        createTestUsers(self)
        createRegion()
        createTestPostcodes()
    
    @attr('the')
    def test_edit_appointment(self):
        """ Makes one appointment and edits that appointment."""
        driver = self.driver
        self.login('steven', 'jansteven')
        self.go_to_view('ChooseARegion', args=[20130101, ])
        self.set_select_field('id_region', ZUID_OOST)
        self.clickPrimairyButton()
        self.set_select_field('id_free_space', VRIJDAG_04JAN)
        self.clickPrimairyButton()
        self.set_text_field('id_name', 'Ada Lovelace')
        self.set_text_field('id_postcode', '1102AB')
        self.set_text_field('id_number', "144")
        self.set_text_field('id_additions', "sous")
        self.set_text_field('id_phone', '020-7123456')
        self.set_text_field('id_stuff', "Bed, boeken en servies")
        self.set_text_field('id_notes', "Lift aanwezig")
        self.sleep()
        self.clickPrimairyButton()
        self.sleep()
        # Appointment has been saved
        driver.find_element_by_link_text("Afspraak zoeken").click()
        self.sleep()        
        self.set_text_field('id_name', "lovelac")
        driver.find_element_by_css_selector("button.btn").click()
        self.sleep()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Bed, boeken en servies")
        self.assertBobyContains("4 januari")
        self.go_to_view('AppointmentEdit', kwargs={ 'appointment_id':1, 'date_iso':20130101})
        self.set_text_field('id_stuff', "Bed, boeken, servies en magnetron")
        self.clickPrimairyButton()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Bed, boeken, servies en magnetron")
        self.go_to_view('AppointmentEdit', kwargs={ 'appointment_id':1, 'date_iso':20130101})
        self.set_select_field("id_free_space", VR_11JAN)
        self.clickPrimairyButton()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Bed, boeken, servies en magnetron")
        self.assertBobyContains("11 januari")
    
    def test_edit_big_appointment(self):
        """ Makes one big appointment and edits that appointment."""
        driver = self.driver
        self.login('steven', 'jansteven')
        self.go_to_view('ChooseARegion', args=[20130101, ])
        self.set_select_field('id_region', ZUID_OOST)
        self.set_select_field("id_weight", "Een dagdeel")
        self.clickPrimairyButton()
        self.sleep()
        self.set_select_field('id_free_space', VRIJDAG_04JAN)
        self.clickPrimairyButton()
        self.sleep()
        self.set_text_field('id_name', 'Ada Lovelace')
        self.set_text_field('id_postcode', '1102AB')
        self.set_text_field('id_number', "144")
        self.set_text_field('id_additions', "sous")
        self.set_text_field('id_phone', '020-7123456')
        self.set_text_field('id_stuff', "Bed, boeken en servies")
        driver.find_element_by_id("id_notes").clear()
        driver.find_element_by_id("id_notes").send_keys("Lift aanwezig")
        self.clickPrimairyButton()
        self.sleep()
        # Appointment has been saved
        driver.find_element_by_link_text("Afspraak zoeken").click()
        self.sleep()        
        self.set_text_field('id_name', "lovelac")
        driver.find_element_by_css_selector("button.btn").click()
        self.sleep()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Bed, boeken en servies")
        self.assertBobyContains("4 januari")
        
        self.go_to_view('AppointmentEdit', kwargs={ 'appointment_id':1, 'date_iso':20130101})
        driver.find_element_by_id("id_stuff").clear()
        self.clickPrimairyButton()
        self.set_text_field("id_stuff", "Bed, boeken, servies en magnetron")
        self.clickPrimairyButton()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Bed, boeken, servies en magnetron")
        
        self.go_to_view('AppointmentEdit', kwargs={ 'appointment_id':1, 'date_iso':20130101})
        self.set_select_field("id_free_space", VR_11JAN)
        self.clickPrimairyButton()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Bed, boeken, servies en magnetron")
        self.assertBobyContains("11 januari")  
            

@attr('selenium', 'viewers')
class ViewersTestCase(DjangoSeleniumTest):
    """ Planner selenium test """
    
    def setUp(self):
        createRegion()
        createTestPostcodes()
        createTestUsers(self)
    
    def test_view_one_appointment(self):
        """ Makes one appointment and edits that appointment."""
        driver = self.driver
        self.login('steven', 'jansteven')
        self.go_to_view('ChooseARegion', args=[20130101, ])
        self.set_select_field('id_region', ZUID_OOST)
        self.clickPrimairyButton()
        self.set_select_field('id_free_space', VRIJDAG_04JAN)
        self.clickPrimairyButton()
        self.set_text_field('id_name', 'Ada Lovelace')
        self.set_text_field('id_postcode', '1102AB')
        self.set_text_field('id_number', "144")
        self.set_text_field('id_additions', "sous")
        self.set_text_field('id_phone', '020-7123456')
        self.set_text_field('id_stuff', "Bed, boeken en servies")
        driver.find_element_by_id("id_notes").clear()
        driver.find_element_by_id("id_notes").send_keys("Lift aanwezig")
        self.clickPrimairyButton()
        # Appointment has been saved
        self.logout()
        self.login("alien", "jansteven")
        self.go_to_view('WeekView', args=[1, 0, 20130101])
        driver.find_element_by_link_text("Vrijdag 4 jan").click()
        self.sleep()
        self.assertBobyContains("Ada Lovelace")
        self.assertBobyContains("Bed, boeken en servies")
        self.assertBobyContains("4 januari")
            
