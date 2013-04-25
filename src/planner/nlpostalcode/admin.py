from __future__ import absolute_import
from .models import Country, Province, City, Cityname, Postcode, \
Street 
from django.contrib import admin

class CitynameAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    ordering = ('name',)
    search_fields = ('name',)
 
 
class CitynameInline(admin.TabularInline):
    model = Cityname
       
class CityAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    
    inlines = [ CitynameInline, ]
    
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id',)
    
class PostcodeAdmin(admin.ModelAdmin):
    pass

class ProvinceAdmin(admin.ModelAdmin):
    pass

class StreetAdmin(admin.ModelAdmin):
    pass


    
admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Cityname, CitynameAdmin)
admin.site.register(Postcode, PostcodeAdmin)
admin.site.register(Street, StreetAdmin)
