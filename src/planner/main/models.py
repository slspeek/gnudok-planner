from __future__ import absolute_import
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import CharField
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.utils.encoding import smart_unicode
import re
from django import forms
from .__init__ import float_to_time


pc_re = re.compile('^\d{4}[A-Z]{2}$')
sofi_re = re.compile('^\d{9}$')
numeric_re = re.compile('^\d+$')


class NLPhoneNumberField(forms.CharField):
    """
    A Dutch telephone number field.
    """
    default_error_messages = {
        'invalid': _('Enter a valid phone number'),
    }

    def clean(self, value):
        super(NLPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''

        phone_nr = re.sub('[\-\s\(\)]', '', smart_unicode(value))

        if len(phone_nr) == 10 and numeric_re.search(phone_nr):
            return value

        if phone_nr[:3] == '+31' and \
                len(phone_nr) == 12 and \
                numeric_re.search(phone_nr[3:]):
            return value

        raise ValidationError(self.error_messages['invalid'])


class PhoneNumberField(CharField):

    description = _("Phone number")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super(PhoneNumberField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': NLPhoneNumberField}
        defaults.update(kwargs)
        return super(PhoneNumberField, self).formfield(**defaults)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^planner.main\.models\.PhoneNumberField"])


class Customer(models.Model):
    """ Representa a customer """
    postcode = models.CharField(_('postalcode'), max_length=14)
    number = models.CharField(_('number'), max_length=10)
    additions = models.CharField(_('additions'), max_length=10, blank=True)
    name = models.CharField(_('name'), max_length=30)
    address = models.CharField(_('address'), max_length=120)
    town = models.CharField(_('town'), max_length=120)
    phone = PhoneNumberField()
    email = models.EmailField(_('email'), max_length=120, blank=True)

    def __str__(self):
        return self.name

    def get_address_display(self):
        if self.additions:
            return u'%s %s - %s' % (self.address, self.number, self.additions)
        else:
            return u'%s %s' % (self.address, self.number)

    class Meta:
        unique_together = (("postcode", "number", "additions"),)


class TimeSlot(models.Model):
    CHOICES = ((1, _("Monday")),
               (2, _("Tuesday")),
               (3, _("Wednesday")),
               (4, _("Thursday")),
               (5, _("Friday")))
    day_of_week = models.IntegerField(choices=CHOICES)
    begin = models.FloatField()
    end = models.FloatField()

    def get_begin_display(self):
        return float_to_time(self.begin)

    def get_end_display(self):
        return float_to_time(self.end)

    def __str__(self):
        return u"%s :  %s - %s" % (self.get_day_of_week_display(),
                                   float_to_time(self.begin),
                                   float_to_time(self.end))


class Region(models.Model):
    name = models.CharField(_('name'), max_length=120, unique=True)
    description = models.TextField(_('description'))

    def __str__(self):
        return "%s: %s" % (self.name, self.description)


class Car(models.Model):
    name = models.CharField(_('name'), max_length=20)

    def __str__(self):
        return self.name


class Rule(models.Model):
    car = models.ForeignKey(Car, verbose_name=_('car'))
    timeslot = models.ForeignKey(TimeSlot, verbose_name=_('timeslot'))
    region = models.ForeignKey(Region, verbose_name=_('region'))
    active = models.BooleanField(default=True, verbose_name=_('active'))

    def __str__(self):
        return u"(%s, %s, %s)" % \
            (str(self.car), str(self.timeslot), str(self.region))


class Calendar(models.Model):
    date = models.DateField(_('date'))
    car = models.ForeignKey(Car, verbose_name=_('car'))
    timeslot = models.ForeignKey(TimeSlot, verbose_name=_('timeslot'))

    def active_appointments(self):
        return Appointment.actives.filter(calendar=self)

    def __str__(self):
        return u"%s: %s - %s" %\
            (self.date.strftime('%d %b '), str(self.timeslot), str(self.car))

    class Meta:
        unique_together = (("date", "car", "timeslot"),)
        ordering = ['date', 'timeslot__begin']


class ActiveManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        query_set = super(ActiveManager, self).get_query_set()
        return query_set.filter(status=self.model.NORMAL).order_by('kind', 'customer__postcode')


class Appointment(models.Model):
    objects = models.Manager()
    actives = ActiveManager()

    calendar = models.ForeignKey(Calendar, verbose_name=_('calendar'))
    customer = models.ForeignKey(Customer, verbose_name=_('customer'))
    employee = models.ForeignKey(User, verbose_name=_('employee'))
    KIND_CHOICES = ((1, _("Delivery")),
                    (2, _("Pick up")),)
    kind = models.IntegerField(_('kind'), choices=KIND_CHOICES, default=2)
    NORMAL = 1
    CANCELLED = 2
    STATUS_CHOICES = ((1, _("Normal")),
                      (2, _("Cancelled")),)
    status = models.IntegerField(_('status'),
                                 choices=STATUS_CHOICES, default=NORMAL)
    CHOICES = ((1, _("Normal")),
               (2, _("Double")),
               (3, _("Tripel")),
               (4, _("Entire half-day")),)
    weight = models.IntegerField(_('weight'), choices=CHOICES, default=1)
    stuff = models.TextField(_('stuff'))
    notes = models.TextField(_('notes'), blank=True)
    created = models.DateTimeField(_("created"),
                                   default=lambda: datetime.datetime.now())

    def __str__(self):
        return self.get_kind_display() + ", " + self.customer.name + ", " + self.stuff

    class Meta:
        ordering = ['kind', 'customer__postcode']
