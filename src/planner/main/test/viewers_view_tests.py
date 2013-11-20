'''
Test for the function that saves the Customer, Appointment and Calendar objects.
'''
from __future__ import absolute_import
from nose.plugins.attrib import attr
from django_webtest import WebTest
import datetime
from .__init__ import ADA_LOVELACE, createTestUsers, createRegion, adaMakesAppointment, adaCancelsAppointment, adaBooksDelivery
from django.core.urlresolvers import reverse
from planner.main.viewers_views import appointment_detail
from planner.main.models import Appointment

@attr('functional', 'kind')
class OrderOnKind(WebTest):
    
    def setUp(self):
        super(OrderOnKind, self).setUp()
        createRegion(self)
        createTestUsers(self)
        adaMakesAppointment(self)
        adaBooksDelivery(self)
         
    def testOrder(self):
        appList = self.calendar.active_appointments().all()
        assert len(appList) == 2
        delivery = appList[0]
        pickup = appList[1]
        self.assertEqual(delivery.kind, 1)
        self.assertEqual(pickup.kind, 2)
        

@attr('functional', 'webtest', 'wsearch')
class Search(WebTest):
    
    def setUp(self):
        super(Search, self).setUp()
        createRegion(self)
        createTestUsers(self)
        adaMakesAppointment(self)
         
    def login_viewer(self):
        login = self.app.get(reverse('Search', args=[], kwargs={ 'date_iso':'20130104'})).follow()
        login_form = login.form
        login_form['username'] = 'alien'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        search = redirect.follow()
        return search

    def testSearchOnName(self):
        """ Search on name"""
        search = self.login_viewer()
        search_form = search.form
        search_form['name'] = 'lac'
        results_page = search_form.submit()
        assert ADA_LOVELACE in results_page
        
    def testSearchOnPostcode(self):
        """ Search on ill-entered postcode"""
        search = self.login_viewer()
        search_form = search.form
        search_form['postcode'] = '1102 a B'
        results_page = search_form.submit()
        assert ADA_LOVELACE in results_page
        
    def testSearchOnStuff(self):
        """ Search on stuff"""
        search = self.login_viewer()
        search_form = search.form
        search_form['stuff'] = 'machine'
        results_page = search_form.submit()
        assert ADA_LOVELACE in results_page
    
    def testSearchOnTown(self):
        """ Search on town"""
        search = self.login_viewer()
        search_form = search.form
        search_form['town'] = 'dam'
        results_page = search_form.submit()
        assert ADA_LOVELACE in results_page
        
    def testSearchHidesPast(self):
        """ Search hides the past"""
        login = self.app.get(reverse('Search', args=[], kwargs={ 'date_iso':'20130106'})).follow()
        login_form = login.form
        login_form['username'] = 'alien'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        search = redirect.follow()
        search_form = search.form
        search_form['town'] = 'dam'
        results_page = search_form.submit()
        assert "0 afspraken gevonden" in results_page
        
    def testCanSearchInPast(self):
        """ Search hides the past"""
        login = self.app.get(reverse('Search', args=[], kwargs={ 'date_iso':'20130106'})).follow()
        login_form = login.form
        login_form['username'] = 'alien'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        search = redirect.follow()
        search_form = search.form
        search_form['town'] = 'dam'
        search_form['include_past'] = True
        results_page = search_form.submit()
        assert ADA_LOVELACE in results_page

    def testSearchOnPhoneNumber(self):
        """ Search on phonenumber """
        search = self.login_viewer()
        search_form = search.form
        search_form['phone'] = '06-12345678'
        results_page = search_form.submit()
        assert ADA_LOVELACE in results_page
        
@attr('functional', 'wsearch', 'cancelled')
class SearchCancelled(WebTest):
    
    def setUp(self):
        super(SearchCancelled, self).setUp()
        createRegion(self)
        createTestUsers(self)
        adaCancelsAppointment(self)
         
    def login_viewer(self):
        login = self.app.get(reverse('Search', args=[], kwargs={ 'date_iso':'20130102'})).follow()
        login_form = login.form
        login_form['username'] = 'alien'
        login_form['password'] = 'jansteven'
        redirect = login_form.submit()
        search = redirect.follow()
        return search

    def testSearchOnNameDoesNotShow(self):
        """ Search on name"""
        search = self.login_viewer()
        search_form = search.form
        search_form['name'] = 'lac'
        results_page = search_form.submit()
        assert not ADA_LOVELACE in results_page
        
    def testSearchOnNameInCancelled(self):
        """ Search on name"""
        search = self.login_viewer()
        search_form = search.form
        search_form['name'] = 'lac'
        search_form['include_cancelled'] = True
        results_page = search_form.submit()
        assert ADA_LOVELACE in results_page
             
        
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
        assert ADA_LOVELACE in details
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
        assert ADA_LOVELACE in details
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
        assert ADA_LOVELACE in details
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
        assert not ADA_LOVELACE in details
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
        assert ADA_LOVELACE in details
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
        assert not ADA_LOVELACE in details
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
        form['employee'] = u'1000'
        details = form.submit().follow()
        assert ADA_LOVELACE in details
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
        assert ADA_LOVELACE in details
        

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
        assert not ADA_LOVELACE in details
        
    
        

