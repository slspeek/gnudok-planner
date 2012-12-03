from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import Select

import time
from .tests import RegionFactory, TimeSlotFactory, CarFactory, RuleFactory


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


class SeleniumTestCase(DjangoSeleniumTest):
    """ Planner selenium test """
    fixtures = ['test_data.json']
    
    def setUp(self):
        self.region = RegionFactory(name='Zuid-Oost', description='Zuid-Oost') 
        self.timeslot = TimeSlotFactory(day_of_week=5,begin=9.0,end=12.5)
        self.car = CarFactory(name='Zeeburg')
        self.rule = RuleFactory(timeslot=self.timeslot, car=self.car, region=self.region)

    def test_make_one_appointment(self):
        """ Makes one appointment and verifies that the details are shown in the listing for that car """
        driver = self.driver
        driver.get(self.live_server_url + "/accounts/login/?next=/main/region/20130101")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("steven")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("jansteven")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        time.sleep(1)
        Select(driver.find_element_by_id("id_region")).select_by_visible_text("Zuid-Oost")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        Select(driver.find_element_by_name("free_space")).select_by_visible_text("11 January Friday : 9 - 12")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("Frederik Jansen")
        driver.find_element_by_id("id_postcode").clear()
        driver.find_element_by_id("id_postcode").send_keys("1102AB")
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("Bijlmerdreef")
        driver.find_element_by_id("id_town").clear()
        driver.find_element_by_id("id_town").send_keys("Amsterdam-Zuidoost")
        driver.find_element_by_id("id_number").clear()
        driver.find_element_by_id("id_number").send_keys("144")
        driver.find_element_by_id("id_additions").clear()
        driver.find_element_by_id("id_additions").send_keys("sous")
        driver.find_element_by_id("id_phone").clear()
        driver.find_element_by_id("id_phone").send_keys("020-123456")
        driver.find_element_by_id("id_stuff").clear()
        driver.find_element_by_id("id_stuff").send_keys("Bed, boeken en servies")
        driver.find_element_by_id("id_notes").clear()
        driver.find_element_by_id("id_notes").send_keys("Lift aanwezig")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Bed, boeken en servies")
        driver.find_element_by_link_text("Display collect list").click()
        time.sleep(2)
        driver.find_element_by_id("id_date").clear()
        driver.find_element_by_id("id_date").send_keys("2013-01-04")
        time.sleep(1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        driver.find_element_by_link_text("Zeeburg").click()
        time.sleep(1)
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Bed, boeken en servies")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Frederik Jansen")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"1102AB")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Lift aanwezig")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"144")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"sous")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"020-123456")
        
        
    def test_search_appointment(self):
        """ Makes one appointment and verifies that the details are the listing for the drivers """
        driver = self.driver
        driver.get(self.live_server_url + "/accounts/login/?next=/main/region/20130101")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("steven")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("jansteven")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        time.sleep(1)
        Select(driver.find_element_by_id("id_region")).select_by_visible_text("Zuid-Oost")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        Select(driver.find_element_by_name("free_space")).select_by_visible_text("11 January Friday : 9 - 12")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("Frederik Jansen")
        driver.find_element_by_id("id_postcode").clear()
        driver.find_element_by_id("id_postcode").send_keys("1102AB")
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("Bijlmerdreef")
        driver.find_element_by_id("id_town").clear()
        driver.find_element_by_id("id_town").send_keys("Amsterdam-Zuidoost")
        driver.find_element_by_id("id_number").clear()
        driver.find_element_by_id("id_number").send_keys("144")
        driver.find_element_by_id("id_phone").clear()
        driver.find_element_by_id("id_phone").send_keys("020-123456")
        driver.find_element_by_id("id_stuff").clear()
        driver.find_element_by_id("id_stuff").send_keys("Bed, boeken en servies")
        driver.find_element_by_id("id_notes").clear()
        driver.find_element_by_id("id_notes").send_keys("Lift aanwezig")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Bed, boeken en servies")
        driver.find_element_by_link_text("Search customer").click()
        time.sleep(1)        
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("frederik")
        driver.find_element_by_css_selector("button.btn").click()
        time.sleep(1)
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Frederik Jansen")
        


    def test_make_four_appointments(self):
        """ Make four appointments in the same timeslot, region and date to see that that date is no longer 
            suggested """
        driver = self.driver
        driver.get(self.live_server_url + "/accounts/login/?next=/main/region/20130101")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("steven")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("jansteven")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        time.sleep(1)
        Select(driver.find_element_by_id("id_region")).select_by_visible_text("Zuid-Oost")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        Select(driver.find_element_by_name("free_space")).select_by_visible_text("11 January Friday : 9 - 12")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        driver.find_element_by_id("id_name").clear()
        
        driver.find_element_by_id("id_name").send_keys("Frederik Jansen")
        driver.find_element_by_id("id_postcode").clear()
        driver.find_element_by_id("id_postcode").send_keys("1102AB")
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("Bijlmerdreef")
        driver.find_element_by_id("id_town").clear()
        driver.find_element_by_id("id_town").send_keys("Amsterdam-Zuidoost")
        driver.find_element_by_id("id_number").clear()
        driver.find_element_by_id("id_number").send_keys("144")
        driver.find_element_by_id("id_phone").clear()
        driver.find_element_by_id("id_phone").send_keys("020-123456")
        driver.find_element_by_id("id_stuff").clear()
        driver.find_element_by_id("id_stuff").send_keys("Bed, boeken en servies")
        driver.find_element_by_id("id_notes").clear()
        driver.find_element_by_id("id_notes").send_keys("Lift aanwezig")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Bed, boeken en servies")
        driver.get(self.live_server_url + "/main/region/20130101")
        Select(driver.find_element_by_id("id_region")).select_by_visible_text("Zuid-Oost")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        Select(driver.find_element_by_name("free_space")).select_by_visible_text("11 January Friday : 9 - 12")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("Mark de Jong")
        driver.find_element_by_id("id_postcode").clear()
        driver.find_element_by_id("id_postcode").send_keys("1102AT")
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("Ken Saro-Wiwastraat")
        driver.find_element_by_id("id_town").clear()
        driver.find_element_by_id("id_town").send_keys("Amsterdam-Zuidoost")
        driver.find_element_by_id("id_number").clear()
        driver.find_element_by_id("id_number").send_keys("21")
        driver.find_element_by_id("id_phone").clear()
        driver.find_element_by_id("id_phone").send_keys("020-654321")
        driver.find_element_by_id("id_stuff").clear()
        driver.find_element_by_id("id_stuff").send_keys("Speelgoed en ikea meubel")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Speelgoed en ikea meubel")
        driver.get(self.live_server_url + "/main/region/20130101")
        Select(driver.find_element_by_id("id_region")).select_by_visible_text("Zuid-Oost")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        Select(driver.find_element_by_name("free_space")).select_by_visible_text("11 January Friday : 9 - 12")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(3)
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("Lidia van de Heuvel")
        driver.find_element_by_id("id_postcode").clear()
        driver.find_element_by_id("id_postcode").send_keys("1102AX")
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("Raoul Wallenbergstraat")
        driver.find_element_by_id("id_town").clear()
        driver.find_element_by_id("id_town").send_keys("Amsterdam-Zuidoost")
        driver.find_element_by_id("id_number").clear()
        driver.find_element_by_id("id_number").send_keys("17")
        driver.find_element_by_id("id_phone").clear()
        driver.find_element_by_id("id_phone").send_keys("020-654321")
        driver.find_element_by_id("id_stuff").clear()
        driver.find_element_by_id("id_stuff").send_keys("Speelgoed, kastjes en bank")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Speelgoed, kastjes en bank")
        driver.get(self.live_server_url + "/main/region/20130101")
        Select(driver.find_element_by_id("id_region")).select_by_visible_text("Zuid-Oost")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        Select(driver.find_element_by_name("free_space")).select_by_visible_text("11 January Friday : 9 - 12")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("Mirjam de Leeuw")
        driver.find_element_by_id("id_postcode").clear()
        driver.find_element_by_id("id_postcode").send_keys("1102ZA")
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("Chestertonlaan")
        driver.find_element_by_id("id_town").clear()
        driver.find_element_by_id("id_town").send_keys("Amsterdam-Zuidoost")
        driver.find_element_by_id("id_number").clear()
        driver.find_element_by_id("id_number").send_keys("17")
        driver.find_element_by_id("id_phone").clear()
        driver.find_element_by_id("id_phone").send_keys("020-654321")
        driver.find_element_by_id("id_stuff").clear()
        driver.find_element_by_id("id_stuff").send_keys("Dozen met kleren")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Dozen met kleren")
        driver.find_element_by_link_text("Display collect list").click()
        time.sleep(1)
        driver.find_element_by_id("id_date").clear()
        driver.find_element_by_id("id_date").send_keys("2013-01-04")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        driver.find_element_by_link_text("Zeeburg").click()
        time.sleep(1)
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Bed, boeken en servies")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Frederik Jansen")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"1102AB")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"Lift aanwezig")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"144")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"020-123456")
        driver.get(self.live_server_url + "/main/region/20130101")
        Select(driver.find_element_by_id("id_region")).select_by_visible_text("Zuid-Oost")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        try:
            self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"11 January Friday : 9 - 12")
            raise Exception()
        except  Exception:
            pass