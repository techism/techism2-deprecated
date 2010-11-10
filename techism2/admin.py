#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism2.models import Event, Location, Organization, StaticPage, Setting
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['published', 'archived']
    list_display = ['title', 'date_time_begin', 'date_time_end', 'location', 'tags', 'user', 'archived', 'published']
    #list_editable = ['published']

class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name', 'street', 'city']
    list_display = ['name', 'street', 'city']
    
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'url']

class StaticPageAdmin(admin.ModelAdmin):
    list_display = ['name', 'content']

class SettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']

admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(StaticPage, StaticPageAdmin)
admin.site.register(Setting, SettingAdmin)
