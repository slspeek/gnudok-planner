from planner.main.models import Car, TimeSlot, Region, Rule, Customer, Appointment, Calendar
import factory
from django.contrib.auth.models import User
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

def createRegion():
    region = RegionFactory(name='Zuid-Oost', description='Zuid-Oost') 
    timeslot = TimeSlotFactory(day_of_week=5, begin=9.0, end=12.5)
    car = CarFactory(name='Auto Zeeburg')
    rule = RuleFactory(timeslot=timeslot, car=car, region=region)
    interval = IntervalFactory(begin='1102aa', end='1102zz', region=region)
    
        
def createTestUsers(self):
    self.group_callcenter = GroupF(name='Callcenter')
    self.group_viewers = GroupF(name='Viewers')
    self.user_steven = UserF(username='steven', password='pbkdf2_sha256$10000$Hk9LhgRtiFgH$xBWE61JIVu8qVCtqGnwYJ2iLPaPCp1UHipcA01zgPN4=')
    self.user_alien =  UserF(username='alien', password='pbkdf2_sha256$10000$Hk9LhgRtiFgH$xBWE61JIVu8qVCtqGnwYJ2iLPaPCp1UHipcA01zgPN4=')
    self.user_steven.groups = [ self.group_callcenter, self.group_viewers ]
    self.user_steven.save()
    self.user_alien.groups = [ self.group_viewers ]

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
