from planner.main.models import Car, TimeSlot, Region,\
    Rule, Customer, Appointment, Calendar
import factory
import datetime
from django_factory_boy.auth import UserF, GroupF
from planner.nlpostalcode.tests import PostcodeBuilder
from planner.area.test import IntervalFactory


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
    self.interval = IntervalFactory(begin='1102aa',
                                    end='1102zz',
                                    region=self.region)

PASSWORD = 'pbkdf2_sha256$10000$Hk9LhgRtiFgH$x' \
           'BWE61JIVu8qVCtqGnwYJ2iLPaPCp1UHipcA01zgPN4='

def createTestUsers(self):
    self.group_callcenter = GroupF(name='Callcenter')
    self.group_viewers = GroupF(name='Viewers')
    
    self.user_steven = UserF(id=1, username='steven',
                             password=PASSWORD)
    self.user_alien = UserF(username='alien',
                             password=PASSWORD)
    self.user_steven.groups = [self.group_callcenter, self.group_viewers]
    self.user_steven.save()
    self.user_alien.groups = [self.group_viewers]
    self.user_alien.save()


def adaMakesAppointment(self):
    self.date = datetime.date(year=2013, month=01, day=04)
    self.calendar = CalendarFactory(date=self.date, car=self.car, timeslot=self.timeslot)
    self.customer = CustomerFactory(name='Ada Lovelace',
                                    postcode='1102AB',
                                    number=42,
                                    address='Bijlmerdreef',
                                    town='Amsterdam',
                                    phone='06-12345678')
    self.appointment = AppointmentFactory(calendar=self.calendar,
                                          created=datetime.date(year=2012, month=12, day=20),
                                          customer=self.customer,
                                          employee=self.user_steven,
                                          stuff='Virtual Machines',
                                          notes='Lift aanwezig')


def adaMakesBigAppointment(self):
    self.date = datetime.date(year=2013, month=01, day=04)
    self.calendar = CalendarFactory(date=self.date, car=self.car, timeslot=self.timeslot)
    self.customer = CustomerFactory(name='Ada Lovelace',
                                    postcode='1102AB',
                                    number=42,
                                    address='Bijlmerdreef',
                                    town='Amsterdam',
                                    phone='06-12345678')
    self.appointment = AppointmentFactory(calendar=self.calendar,
                                          created=datetime.date(year=2012, month=12, day=20),
                                          customer=self.customer,
                                          employee=self.user_steven,
                                          stuff='Gehele nalatenschap',
                                          weight=4,
                                          notes='Lift aanwezig')


class CarFactory(factory.Factory):
    FACTORY_FOR = Car

    name = "Open source tractor"


class TimeSlotFactory(factory.Factory):
    FACTORY_FOR = TimeSlot

    day_of_week = 1
    begin = 13
    end = 17


class RegionFactory(factory.Factory):
    FACTORY_FOR = Region

    name = "Groot Oost"


class RuleFactory(factory.Factory):
    FACTORY_FOR = Rule

    car = factory.SubFactory(CarFactory)
    region = factory.SubFactory(RegionFactory)
    timeslot = factory.SubFactory(TimeSlotFactory)


class CustomerFactory(factory.Factory):
    FACTORY_FOR = Customer

    name = "Willem Knaap"
    address = "Grachtengordel 1"
    town = "Juinen"
    postcode = "1469 SH"
    phone = "020-6164590"
    email = "wk@example.com"


class CalendarFactory(factory.Factory):
    FACTORY_FOR = Calendar

    date = datetime.date(2012, 10, 29)
    timeslot = factory.SubFactory(TimeSlotFactory)
    car = factory.SubFactory(CarFactory)
    #region = factory.SubFactory(RegionFactory)


class AppointmentFactory(factory.Factory):
    FACTORY_FOR = Appointment

    calendar = factory.SubFactory(CalendarFactory)
    customer = factory.SubFactory(CustomerFactory)
    employee = factory.SubFactory(UserF)
    stuff = "Gold, Platina and lots of Silver"
    notes = "Bring boxes"
    created = datetime.datetime.now()
