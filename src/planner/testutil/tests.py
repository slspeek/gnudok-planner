from planner.main.models import Customer, Calendar
from planner.nlpostalcode.models import Source, Country, Province, City, Cityname, Postcode, Street
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from django.core.urlresolvers import reverse
import os
import time


class DjangoSeleniumTest(LiveServerTestCase):
    """ Base class for the django selenium testing """

    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        super(DjangoSeleniumTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(DjangoSeleniumTest, cls).tearDownClass()

    def tearDown(self):
        super(DjangoSeleniumTest, self).tearDown()
           
        
    def setUp(self):
        Source.objects.all().delete()
        Country.objects.all().delete()
        Province.objects.all().delete()
        Cityname.objects.all().delete()
        City.objects.all().delete()
        Street.objects.all().delete()
        Postcode.objects.all().delete()
        super(DjangoSeleniumTest, self). setUp()

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
        self.sleep()
 
