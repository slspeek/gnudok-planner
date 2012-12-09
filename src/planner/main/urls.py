from __future__ import absolute_import
from django.views.generic.detail import DetailView

from .models import Appointment
from django.conf.urls import patterns, url
from .views import create_appointment, choose_a_date,\
    chose_a_region,\
    edit_appointment
from .viewers_views import display_date_form,\
    render_appointment_list, choose_calendar, \
    calendar_search_view, weekview, overview
    
urlpatterns = patterns('',
    url(r'^app/detail/(?P<pk>\d+)$', DetailView.as_view(model=Appointment), name='AppointmentView'),
    (r'^app/create/(?P<calendar_id>\d+)/(?P<weight>\d+)', create_appointment),
    url(r'^app/edit/(?P<appointment_id>\w+)/(?P<date_iso>\d{0,8})', edit_appointment, name='AppointmentEdit'),
    (r'^date_chosen/(?P<region_id>\d+)/(?P<weight>\d+)/(?P<date_iso>\d{0,8})', choose_a_date),
    (r'^list/choose', display_date_form),
    (r'^list/date_chosen/(?P<date_string>\d{8})', choose_calendar),
    (r'^list/appointments/(?P<calendar_id>\d+)', render_appointment_list),
    url(r'^overview$', overview, name='Overview'),
    (r'^region/(?P<date_iso>\d{0,8})', chose_a_region),
    (r'^search/', calendar_search_view),
    (r'^week/(?P<car_id>\d+)/(?P<offset>[-]?\d+)/(?P<date_iso>\d{0,8})$', weekview),
)
