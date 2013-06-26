""" postal database  from Dutch
    http://www.d-centralize.nl/static/kvdb/mysql_sql.txt.gz """
from django.db import models
from django.utils.encoding import smart_str, smart_unicode

class Source(models.Model):
    """ The wiki source that was for the postalcode information """
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    active = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, unique=True, blank=True)
    source = models.CharField(max_length=255, unique=True, blank=True)
    ip = models.TextField(blank=True)
    wikiuser = models.IntegerField(null=True, blank=True)
    class Meta:
        """ Pins the database table"""
        db_table = u'source'

    def __str__(self):
        return "Source: %d" % self.id

class Country(models.Model):
    """ Models a country for the postal-lookups """
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    active = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, unique=True, blank=True)
    lat = models.DecimalField(null=True, max_digits=12, decimal_places=8, blank=True)
    lng = models.DecimalField(null=True, max_digits=12, decimal_places=8, blank=True)
    source = models.ForeignKey(Source)
    class Meta:
        """ Pins the database table"""
        db_table = u'country'

class Province(models.Model):
    """ County of the postalcode """
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    active = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, unique=True, blank=True)
    lat = models.DecimalField(null=True, max_digits=12, decimal_places=8, blank=True)
    lng = models.DecimalField(null=True, max_digits=12, decimal_places=8, blank=True)
    source = models.ForeignKey(Source)
    country = models.ForeignKey(Country)
    class Meta:
        """ Pins the database table"""
        db_table = u'province'
        
    def __str__(self):
        return self.name


class City(models.Model):
    """ City of the postalcode """
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    active = models.IntegerField(null=True, blank=True)
    source = models.ForeignKey(Source)
    municipality = models.ForeignKey('self', null=True, blank=True)
    municipality_code = models.IntegerField(null=True, blank=True)
    province = models.ForeignKey(Province)
    lat = models.DecimalField(null=True, max_digits=12, decimal_places=8, blank=True)
    lng = models.DecimalField(null=True, max_digits=12, decimal_places=8, blank=True)
    areacode = models.CharField(max_length=30, blank=True)
    
    def get_official_name(self):
        names = self.cityname_set.all()
        official_citynames = filter(lambda x: (x.official == 1),names)
        if official_citynames:
            return smart_str(official_citynames[0].name)
        if names:
            return smart_str(names[0].name)
        return "No given name"   
        
    
    class Meta:
        """ Pins the database table"""
        db_table = u'city'
        
    def __str__(self):
        return '%s' % self.get_official_name()
    
class Cityname(models.Model):
    """ Name of the city """
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    active = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=192, blank=True)
    official = models.IntegerField(null=True, blank=True)
    source = models.ForeignKey(Source)
    city = models.ForeignKey(City)
    class Meta:
        """ Pins the database table"""
        db_table = u'cityname'
    
    def __str__(self):
        return self.name

class Postcode(models.Model):
    """ The postal code """
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    active = models.IntegerField(null=True, blank=True)
    source = models.ForeignKey(Source)
    fourpp = models.IntegerField(unique=True, null=True, blank=True)
    lat = models.DecimalField(null=True, max_digits=12, decimal_places=8, blank=True)
    lng = models.DecimalField(null=True, max_digits=12, decimal_places=8, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    class Meta:
        """ Pins the database table"""
        db_table = u'postcode'
        
        ordering = ['fourpp']

    def __str__(self):
        return "%s %s" % (self.fourpp, self.city.get_official_name())

class Street(models.Model):
    """ Street of the postalcode """
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    active = models.IntegerField(null=True, blank=True)
    source = models.ForeignKey(Source)
    chars = models.CharField(max_length=6, blank=True)
    street = models.CharField(max_length=765, blank=True)
    even = models.IntegerField(null=True, blank=True)
    low = models.IntegerField(null=True, blank=True)
    high = models.IntegerField(null=True, blank=True)
    lowcapped = models.IntegerField(null=True, blank=True)
    highcapped = models.IntegerField(null=True, blank=True)
    lat = models.DecimalField(null=True, max_digits=12, decimal_places=8, blank=True)
    lng = models.DecimalField(null=True, max_digits=12, decimal_places=8, blank=True)
    postcode = models.ForeignKey(Postcode, null=True, blank=True)
    pobox = models.IntegerField(null=True, blank=True)
    unsure = models.IntegerField(null=True, blank=True)
    subtitle = models.CharField(max_length=765, blank=True)
    class Meta:
        """ Pins the database table"""
        db_table = u'street'
        
    def __str__(self):
        return "%s %s-%s %s %s %s" % (smart_str(self.street),
                                       self.low,
                                        self.high,
                                         self.postcode.fourpp,
                                         self.chars,
                                         self.postcode.city.get_official_name(),
                                          )
