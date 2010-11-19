#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism2.models import Event, EventChangeLog, Location, Organization, StaticPage, Setting, TweetedEvent
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['published', 'archived']
    list_display = ['title', 'date_time_begin', 'date_time_end', 'location', 'tags', 'user', 'archived', 'published']
    #list_editable = ['published']

class EventChangeLogAdmin(admin.ModelAdmin):
    list_filter = ['change_type']
    list_display = ['event', 'event_title', 'change_type', 'date_time']

class TweetedEventAdmin(admin.ModelAdmin):
    list_display = ['event', 'tweet', 'date_time_created']

class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name', 'street', 'city']
    list_display = ['name', 'street', 'city']
    
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'url', 'tags']

class StaticPageAdmin(admin.ModelAdmin):
    list_display = ['name', 'content']

class SettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']

admin.site.register(Event, EventAdmin)
admin.site.register(EventChangeLog, EventChangeLogAdmin)
admin.site.register(TweetedEvent, TweetedEventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(StaticPage, StaticPageAdmin)
admin.site.register(Setting, SettingAdmin)
