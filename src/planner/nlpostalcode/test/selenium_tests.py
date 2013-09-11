from planner.testutil.tests import DjangoSeleniumTest
from nose.plugins.attrib import attr
from planner.main.test.__init__ import createRootUser, createTestUsers, createRegion, createRegionEast, createTestPostcodes, adaMakesAppointment, adaMakesBigAppointment

@attr('selenium', 'zouhair')
class PostcodeAdmin(DjangoSeleniumTest):
    """ Hello selenium """
    
    def setUp(self):
        super(PostcodeAdmin, self).setUp()
        createRootUser(self)
        
        
    def test_logon_as_root_in_admin(self):
        self.driver.get(self.live_server_url + "/admin/")
        self.sleep();
        self.driver.find_element_by_id("id_username").clear()
        self.driver.find_element_by_id("id_username").send_keys("root")
        self.driver.find_element_by_id("id_password").clear()
        self.driver.find_element_by_id("id_password").send_keys("root")
        self.driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        #self.driver.find_element_by_link_text("Afmelden").click()
        self.sleep()
        self.driver.find_element_by_link_text("Nlpostalcode").click()
        self.sleep()

        #Source
        driver = self.driver
        driver.find_element_by_xpath("(//a[contains(text(),'Toevoegen')])[6]").click()
        self.sleep();
        driver.find_element_by_id("id_id").clear()
        driver.find_element_by_id("id_id").send_keys("1")
        driver.find_element_by_link_text("Vandaag").click()
        driver.find_element_by_link_text("Nu").click()
        driver.find_element_by_css_selector("div.form-row.field-updated > div > p.datetime > span.datetimeshortcuts > a").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Nu')])[2]").click()
        driver.find_element_by_id("id_active").clear()
        driver.find_element_by_id("id_active").send_keys("1")
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("Angelique")
        driver.find_element_by_id("id_source").clear()
        driver.find_element_by_id("id_source").send_keys("1")
        driver.find_element_by_id("id_ip").clear()
        driver.find_element_by_id("id_ip").send_keys("123.123.123.123")
        driver.find_element_by_name("_save").click()
        self.sleep()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*Angelique[\s\S]*$")
        
        #Country
        driver.get(self.live_server_url + "/admin/nlpostalcode/")
        driver.find_element_by_xpath("(//a[contains(text(),'Toevoegen')])[3]").click()
        self.sleep();
        driver.find_element_by_id("id_id").clear()
        driver.find_element_by_id("id_id").send_keys("1")
        driver.find_element_by_link_text("Vandaag").click()
        driver.find_element_by_link_text("Nu").click()
        driver.find_element_by_css_selector("div.form-row.field-updated > div > p.datetime > span.datetimeshortcuts > a").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Nu')])[2]").click()
        driver.find_element_by_id("id_active").clear()
        driver.find_element_by_id("id_active").send_keys("1")
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("North Korea")
        select_source_elem = driver.find_element_by_id("id_source")
        select_source_elem.send_keys("Source: 1")
        driver.find_element_by_name("_save").click()
        self.sleep()
        
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*North Korea[\s\S]*$")
        
        
        ############################################################################################################
        
        #Province
        driver.get(self.live_server_url + "/admin/nlpostalcode/")
        driver.find_element_by_xpath("(//a[contains(text(),'Toevoegen')])[5]").click()
        self.sleep();
        driver.find_element_by_id("id_id").clear()
        driver.find_element_by_id("id_id").send_keys("2")
        driver.find_element_by_link_text("Vandaag").click()
        driver.find_element_by_link_text("Nu").click()
        driver.find_element_by_css_selector("div.form-row.field-updated > div > p.datetime > span.datetimeshortcuts > a").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Nu')])[2]").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("Noord Holland")
        select_source_elem = driver.find_element_by_id("id_source")
        select_source_elem.send_keys("Source: 1")
        select_country_elem = driver.find_element_by_id("id_country")
        select_country_elem.send_keys("North Korea")
        driver.find_element_by_name("_save").click()
        self.sleep()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*Noord Holland[\s\S]*$")

        #City
        driver.get(self.live_server_url + "/admin/nlpostalcode/")
        driver.find_element_by_xpath("(//a[contains(text(),'Toevoegen')])[2]").click()
        self.sleep();
        driver.find_element_by_id("id_id").clear()
        driver.find_element_by_id("id_id").send_keys("1")
        driver.find_element_by_link_text("Vandaag").click()
        driver.find_element_by_link_text("Nu").click()
        driver.find_element_by_css_selector("div.form-row.field-updated > div > p.datetime > span.datetimeshortcuts > a").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Nu')])[2]").click()
        select_source_elem = driver.find_element_by_id("id_source")
        select_source_elem.send_keys("Source: 1")
        select_country_elem = driver.find_element_by_id("id_province")
        select_country_elem.send_keys("Noord Holland")
        driver.find_element_by_name("_save").click()
        self.sleep()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*No given name[\s\S]*$")

        #Citynames
        driver.get(self.live_server_url + "/admin/nlpostalcode/")
        driver.find_element_by_link_text("Toevoegen").click()
        self.sleep();
        driver.find_element_by_id("id_id").clear()
        driver.find_element_by_id("id_id").send_keys("1")
        driver.find_element_by_link_text("Vandaag").click()
        driver.find_element_by_link_text("Nu").click()
        driver.find_element_by_css_selector("div.form-row.field-updated > div > p.datetime > span.datetimeshortcuts > a").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Nu')])[2]").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("Amsterdam")
        select_source_elem = driver.find_element_by_id("id_source")
        select_source_elem.send_keys("Source: 1")
        select_city_elem = driver.find_element_by_id("id_city")
        select_city_elem.send_keys("No given name")
        driver.find_element_by_name("_save").click()
        self.sleep()      
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*Amsterdam[\s\S]*$")
        
        #Postcode
        driver.get(self.live_server_url + "/admin/nlpostalcode/")
        driver.find_element_by_xpath("(//a[contains(text(),'Toevoegen')])[4]").click()
        self.sleep()
        driver.find_element_by_id("id_id").clear()
        driver.find_element_by_id("id_id").send_keys("1")
        driver.find_element_by_link_text("Vandaag").click()
        driver.find_element_by_link_text("Nu").click()
        driver.find_element_by_css_selector("div.form-row.field-updated > div > p.datetime > span.datetimeshortcuts > a").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Nu')])[2]").click()
        select_source_elem = driver.find_element_by_id("id_source")
        select_source_elem.send_keys("Source: 1")
        driver.find_element_by_id("id_fourpp").clear()
        driver.find_element_by_id("id_fourpp").send_keys("666")
        select_city_elem = driver.find_element_by_id("id_city")
        select_city_elem.send_keys("Amsterdam")
        driver.find_element_by_name("_save").click()
        self.sleep()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*666[\s\S]*$")

        
        #Street
        driver.get(self.live_server_url + "/admin/nlpostalcode/")
        driver.find_element_by_xpath("(//a[contains(text(),'Toevoegen')])[7]").click()
        self.sleep()
        driver.find_element_by_id("id_id").clear()
        driver.find_element_by_id("id_id").send_keys("1")
        driver.find_element_by_link_text("Vandaag").click()
        driver.find_element_by_link_text("Nu").click()
        driver.find_element_by_css_selector("div.form-row.field-updated > div > p.datetime > span.datetimeshortcuts > a").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Nu')])[2]").click()
        select_source_elem = driver.find_element_by_id("id_source")
        select_source_elem.send_keys("Source: 1")
        driver.find_element_by_id("id_street").clear()
        driver.find_element_by_id("id_street").send_keys("Axis of Evil Lane")
        driver.find_element_by_id("id_chars").clear()
        driver.find_element_by_id("id_chars").send_keys("BZ")
        select_city_elem = driver.find_element_by_id("id_postcode")
        select_city_elem.send_keys("666 Amsterdam")
        driver.find_element_by_name("_save").click()
        self.sleep()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*Axis of Evil Lane[\s\S]*$")

