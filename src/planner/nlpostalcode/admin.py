from __future__ import absolute_import
from .models import Country, Province, City, \
Cityname, Postcode, Street, Source
from django.contrib import admin

class CitynameAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    ordering = ('name',)
    search_fields = ('name',)
 
class CitynameInline(admin.TabularInline):
    model = Cityname
    
class StreetInline(admin.TabularInline):
    model = Street
     
class CityAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    search_fields = ('cityname__name',)
    inlines = [ CitynameInline, ]
    
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class PostcodeAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    ordering = ('fourpp',)
    search_fields = ['fourpp',]
    #inlines = [ StreetInline, ]

class ProvinceAdmin(admin.ModelAdmin):
    pass

class StreetAdmin(admin.ModelAdmin):
    #list_display = ('low', 'high', 'street', )
    ordering = ('street',)
    search_fields = ['^street', '=chars',]
    
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Cityname, CitynameAdmin)
admin.site.register(Postcode, PostcodeAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(Source, SourceAdmin)
