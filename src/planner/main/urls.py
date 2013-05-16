from __future__ import absolute_import
from .models import Appointment
from django.conf.urls import patterns, url
from .views import cancel_appointment
from .viewers_views import display_date_form,\
    render_appointment_list, choose_calendar, \
    calendar_search_view, weekview, overview, \
    appointment_detail, appointments_by_date, \
    appointments_made_by, choose_an_employee, wrong_postcode
from .views import appointment_manipulation
from .views import get_available_dates, get_customer
    

urlpatterns = patterns('',
    
    (r'^get_available_dates/(?P<postalcode>\w*)/(?P<weight>\d+)/(?P<date_iso>\d{0,8})/(?P<calendar_id>[-]?\d+)/(?P<unrestricted>\w*)', get_available_dates),
    (r'^get_customer/(?P<postalcode>\w+)/(?P<number>\w+)/(?P<addition>\w*)', get_customer),
    url(r'^app/detail/(?P<pk>\d+)$', appointment_detail, name='AppointmentView'),
    url(r'^edit/(?P<appointment_id>\w+)/(?P<customer_id>\w+)/(?P<date_iso>\d{0,8})', appointment_manipulation, name='AppointmentEditExtra'),
    (r'^list/choose', display_date_form),
    (r'^list/date_chosen/(?P<date_string>\d{8})', choose_calendar),
    (r'^list/appointments/(?P<calendar_id>\d+)', render_appointment_list),
    url(r'^app/cancel/(?P<appointment_id>\d+)', cancel_appointment, name="CancelAppointment"),
    url(r'^overview/(?P<date_iso>\d{0,8})$', overview, name='Overview'),
    url(r'^search/(?P<date_iso>\d{0,8})$', calendar_search_view, name='Search'),
    url(r'^week/(?P<car_id>\d+)/(?P<offset>[-]?\d+)/(?P<date_iso>\d{0,8})$', weekview, name='WeekView'),
    url(r'^made_at/(?P<date_iso>\d{0,8})$', appointments_by_date, name='AppointmentsToday'),
    url(r'^made_by/(?P<employee_id>\d+)', appointments_made_by, name='AppointmentsMadeBy'),
    url(r'^employee/', choose_an_employee, name='ChooseAnEmployee'),
    url(r'^wrong/', wrong_postcode, name='WrongPostcode'),
)
