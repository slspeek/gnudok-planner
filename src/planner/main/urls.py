from __future__ import absolute_import
from django.views.generic.detail import DetailView

from .models import Appointment
from django.conf.urls import patterns, url
from .views import create_appointment, chosen_date, display_date_form,\
    render_appointment_list, list_date_chosen, chose_a_region,\
    calendar_search_view
urlpatterns = patterns('',

    url(r'^app/detail/(?P<pk>\d+)$', DetailView.as_view(model=Appointment), name='AppointmentView'),
    (r'^app/create/', create_appointment),
    (r'^date_chosen/(?P<date_iso>\d{0,8})', chosen_date),
    (r'^list/choose', display_date_form),
    (r'^list/date_chosen/', list_date_chosen),
    (r'^list/appointments', render_appointment_list),
    (r'^region/(?P<date_iso>\d{0,8})', chose_a_region),
    (r'^search/', calendar_search_view),
     
)
