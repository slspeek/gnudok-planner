# -*- coding: utf-8 -*-
import factory
from planner.main.models import Car, TimeSlot, Region, Rule, Customer, Appointment, Calendar
import datetime
from django_factory_boy.auth import UserFactory
from planner.nlpostalcode.tests import PostcodeBuilder
from planner.area.test import IntervalFactory
from django.contrib.auth.models import User, Permission

ADA_LOVELACE=u'Adå Lŏvelace'


def createTestPostcodes():
    builder = PostcodeBuilder()
    code = builder.create_amsterdam_postcode_number(1102)
    builder.create_street(code, 'Bijlmerdreef', 'ab')
    builder.create_street(code, 'Ken Saro-Wiwastraat', 'at')
    builder.create_street(code, 'Raoul Wallenbergstraat', 'ax')
    builder.create_street(code, 'Chestertonlaan', 'za')


def createRegion(self):
    self.region = RegionFactory(name='Zuid-Oost', description='Zuid-Oost')
    self.timeslot = TimeSlotFactory(day_of_week=5, begin=9.0, end=12.5)
    self.car = CarFactory(name='Auto Zeeburg')
    self.rule = RuleFactory(timeslot=self.timeslot,
                            car=self.car,
                            region=self.region)
    self.interval = IntervalFactory(begin='1100aa',
                                    end='1102zz',
                                    region=self.region)

def createRegionEast(self):
    self.region = RegionFactory(name='Oost', description='Oost')
    self.timeslot = TimeSlotFactory(day_of_week=4, begin=9.0, end=12.5)
    self.car = CarFactory(name='Auto Zeeburg')
    self.rule = RuleFactory(timeslot=self.timeslot,
                            car=self.car,
                            region=self.region)
    self.interval = IntervalFactory(begin='1102aa',
                                    end='1102zz',
                                    region=self.region)

PASSWORD = 'pbkdf2_sha256$10000$Hk9LhgRtiFgH$x' \
           'BWE61JIVu8qVCtqGnwYJ2iLPaPCp1UHipcA01zgPN4='

def createRootUser(self): 
    self.root_user = User.objects.create_superuser('root', 'root@gnu.org', 'root')
    self.root_user.save()
    
def createTestUsers(self):
    #User.objects.all().delete()
    CALLCENTER_PERMISSION=Permission.objects.get(codename='callcenter')
    VIEWERS_PERMISSION=Permission.objects.get(codename='viewers')
    self.user_steven = UserFactory(id=1000, username='steven', password=PASSWORD)
    self.user_alien = UserFactory(id=2000, username='alien',  password=PASSWORD, first_name='Alien')
    self.user_steven.user_permissions.add(VIEWERS_PERMISSION,CALLCENTER_PERMISSION)
    self.user_steven.save()
    self.user_alien.user_permissions.add(VIEWERS_PERMISSION)
    self.user_alien.save()

def createAda(self):
    self.customer = CustomerFactory(name=ADA_LOVELACE,
                           postcode='1102AB',
                           number=42,
                           address='Bijlmerdreef',
                           town='Amsterdam',
                           phone='06-12345678')
    return self.customer

def adaMakesAppointment(self):
    self.date = datetime.date(year=2013, month=01, day=04)
    self.calendar = CalendarFactory(date=self.date, car=self.car, timeslot=self.timeslot)
    self.customer = createAda(self)
    self.appointment = AppointmentFactory(calendar=self.calendar,
                                          created=datetime.date(year=2012, month=12, day=20),
                                          customer=self.customer,
                                          employee=self.user_steven,
                                          stuff='Virtual Machines',
                                          notes='Lift aanwezig')
    self.customer_id_ada = self.customer.id

def adaBooksDelivery(self):
    self.date = datetime.date(year=2013, month=01, day=04)
    self.appointment = AppointmentFactory(calendar=self.calendar,
                                          created=datetime.date(year=2012, month=12, day=20),
                                          customer=self.customer,
                                          employee=self.user_steven,
                                          kind=1,
                                          stuff='Bank',
                                          notes='Lift aanwezig')


def adaMakesBigAppointment(self):
    self.date = datetime.date(year=2013, month=01, day=04)
    self.calendar = CalendarFactory(date=self.date, car=self.car, timeslot=self.timeslot)
    self.customer = createAda(self)
    self.appointment = AppointmentFactory(calendar=self.calendar,
                                          created=datetime.date(year=2012, month=12, day=20),
                                          customer=self.customer,
                                          employee=self.user_steven,
                                          stuff='Gehele nalatenschap',
                                          weight=4,
                                          notes='Lift aanwezig')

def adaCancelsAppointment(self):
    self.date = datetime.date(year=2013, month=01, day=04)
    self.calendar = CalendarFactory(date=self.date, car=self.car, timeslot=self.timeslot)
    self.customer = createAda(self)
    self.appointment = AppointmentFactory(calendar=self.calendar,
                                          created=datetime.date(year=2012, month=12, day=20),
                                          customer=self.customer,
                                          employee=self.user_steven,
                                          stuff='Gehele nalatenschap',
                                          weight=4,
                                          status=2,
                                          notes='Lift aanwezig')


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Car

    name = "Open source tractor"


class TimeSlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TimeSlot

    day_of_week = 1
    begin = 13
    end = 17


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Region

    name = "Groot Oost"


class RuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rule

    car = factory.SubFactory(CarFactory)
    region = factory.SubFactory(RegionFactory)
    timeslot = factory.SubFactory(TimeSlotFactory)


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = "Willem Knaap"
    address = "Grachtengordel 1"
    town = "Juinen"
    postcode = "1469 SH"
    phone = "020-6164590"
    email = "wk@example.com"


class CalendarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Calendar

    date = datetime.date(2012, 10, 29)
    timeslot = factory.SubFactory(TimeSlotFactory)
    car = factory.SubFactory(CarFactory)
    #region = factory.SubFactory(RegionFactory)


class AppointmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Appointment

    calendar = factory.SubFactory(CalendarFactory)
    customer = factory.SubFactory(CustomerFactory)
    employee = factory.SubFactory(UserFactory)
    stuff = "Gold, Platina and lots of Silver"
    notes = "Bring boxes"
    created = datetime.datetime.now()
