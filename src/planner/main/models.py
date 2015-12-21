import re
import django
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import CharField
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django import forms
from planner.main import float_to_time


pc_re = re.compile(r'^\d{4}[A-Z]{2}$')
sofi_re = re.compile(r'^\d{9}$')
numeric_re = re.compile(r'^\d+$')

KIND_DELIVERY = 1
KIND_PICKUP = 2
KIND_CHOICES = ((KIND_DELIVERY, _("Delivery")),
                (KIND_PICKUP, _("Pick up")),)

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
        phone_nr = re.sub(r'[\-\s\(\)]', '', value)

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

    def __unicode__(self):
        return "%s %s" % (self.name, self.get_address_display())

    def get_address_display(self):
        if self.additions:
            return '%s %s - %s' % (self.address, self.number, self.additions)
        else:
            return '%s %s' % (self.address, self.number)

    class Meta(object):
        unique_together = (("postcode", "number", "additions"),)
        permissions = (("viewers", "Viewers"),
                       ("callcenter", "Callcenter"),)

class TimeSlot(models.Model):
    CHOICES = ((1, _("Monday")),
               (2, _("Tuesday")),
               (3, _("Wednesday")),
               (4, _("Thursday")),
               (5, _("Friday")),
               (6, _("Saturday")))
    day_of_week = models.IntegerField(choices=CHOICES)
    begin = models.FloatField()
    end = models.FloatField()

    def get_begin_display(self):
        return float_to_time(self.begin)

    def get_end_display(self):
        return float_to_time(self.end)

    def __unicode__(self):
        return "%s :  %s - %s" % (self.get_day_of_week_display(),
                                  float_to_time(self.begin),
                                  float_to_time(self.end))


class Region(models.Model):
    name = models.CharField(_('name'), max_length=120, unique=True)
    description = models.TextField(_('description'))

    def __unicode__(self):
        return "%s: %s" % (self.name, self.description)


class Car(models.Model):
    name = models.CharField(_('name'), max_length=20)

    def __unicode__(self):
        return "%s" % self.name


class Rule(models.Model):
    car = models.ForeignKey(Car, verbose_name=_('car'))
    timeslot = models.ForeignKey(TimeSlot, verbose_name=_('timeslot'))
    region = models.ForeignKey(Region, verbose_name=_('region'))
    kind = models.IntegerField(_('kind'), choices=KIND_CHOICES, default=2)
    active = models.BooleanField(default=True, verbose_name=_('active'))

    def __unicode__(self):
        return "(%s, %s, %s, %s)" % \
            (self.car, self.get_kind_display(), self.timeslot, self.region)


class Calendar(models.Model):
    date = models.DateField(_('date'))
    car = models.ForeignKey(Car, verbose_name=_('car'))
    timeslot = models.ForeignKey(TimeSlot, verbose_name=_('timeslot'))

    def active_appointments(self):
        # pylint: disable=E1101
        return Appointment.actives.filter(calendar=self)

    def __unicode__(self):
        return "%s: %s - %s" %\
            (self.date.strftime('%d %b '), self.timeslot, self.car)

    class Meta(object):
        unique_together = (("date", "car", "timeslot"),)
        ordering = ['date', 'timeslot__begin']


class ActiveManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        # pylint: disable=E1101
        query_set = super(ActiveManager, self).get_queryset()
        return query_set.filter(status=self.model.NORMAL)


class Appointment(models.Model):
    objects = models.Manager()
    actives = ActiveManager()

    calendar = models.ForeignKey(Calendar, verbose_name=_('calendar'))
    customer = models.ForeignKey(Customer, verbose_name=_('customer'))
    employee = models.ForeignKey(User, verbose_name=_('employee'))
    kind = models.IntegerField(_('kind'), choices=KIND_CHOICES, default=2)
    NORMAL = 1
    CANCELLED = 2
    STATUS_CHOICES = ((NORMAL, _("Normal")),
                      (CANCELLED, _("Cancelled")),)
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
                                   default=django.utils.timezone.now)

    def __unicode__(self):
        return "%s, %s, %s" % (self.get_kind_display(), self.customer.name, self.stuff)

    class Meta(object):
        ordering = ['kind', 'customer__postcode']
