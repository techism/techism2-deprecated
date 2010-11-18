#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models import signals
from django.db import models
from datetime import datetime, timedelta
import time
from techism2 import fields, utils

class Location(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name;
    
    
class Organization (models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    tags = fields.CommaSeparatedListField(models.CharField(max_length=20), blank=True, null=True)
    
    def __unicode__(self):
        return self.title;
    

class Event(models.Model):
    title = models.CharField(max_length=200)
    date_time_begin = models.DateTimeField()
    date_time_end = models.DateTimeField(blank=True, null=True)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    tags = fields.CommaSeparatedListField(models.CharField(max_length=20), blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    archived = models.BooleanField()
    published = models.BooleanField()
    canceled = models.BooleanField()
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    
    def __unicode__(self):
        return self.title
    
    def get_date_time_created_utc(self):
        "Gets the 'Created' date/time in UTC."
        return utils.localize_to_utc(self.date_time_created);
    
    def get_date_time_modified_utc(self):
        "Gets the 'Modifed' date/time in UTC."
        return utils.localize_to_utc(self.date_time_modified);
    
    def get_date_time_begin_utc(self):
        "Gets the 'Begin' date/time in UTC."
        return utils.localize_to_utc(self.date_time_begin);
    
    def get_date_time_begin_cet(self):
        "Gets the 'Begin' date/time in CET/CEST."
        return utils.utc_to_cet(self.date_time_begin);
    
    def set_date_time_begin_cet(self, date_time_begin_cet):
        "Sets the 'Begin' date/time in CET/CEST timezone. Internally the date/time is saved in UTC timezone."
        self.date_time_begin = utils.cet_to_utc(date_time_begin_cet)
    
    def get_date_time_end_utc(self):
        "Gets the 'End' date/time in UTC."
        return utils.localize_to_utc(self.date_time_end);
    
    def get_date_time_end_cet(self):
        "Gets the 'End' date/time in CET/CEST."
        return utils.utc_to_cet(self.date_time_end);
    
    def set_date_time_end_cet(self, date_time_end_cet):
        "Sets the 'End' date/time, expecting CET/CEST timezone. Internally the date/time is saved in UTC timezone"
        self.date_time_end = utils.cet_to_utc(date_time_end_cet)
    
    def update_archived_flag(self):
        "Updates the 'Archived' flag, depending if the the end date is set or not"
        utc = utils.localize_to_utc(datetime.utcnow())
        if self.get_date_time_end_utc():
            self.archived = self.get_date_time_end_utc() < utc
        else:   
            self.archived = self.get_date_time_begin_utc() + timedelta(hours=1) < utc
            
    def takes_more_than_one_day (self):
        if self.date_time_end is None: 
            return False;
        elif (self.get_date_time_end_cet().weekday() == self.get_date_time_begin_cet().weekday()):
            return False;
        else:
            return True;
        
    def getNumberOfDays (self):
        if (self.takes_more_than_one_day()):
            return (self.get_date_time_end_cet().date() - self.get_date_time_begin_cet().date()).days + 1
        else:
            return 0;
                                            

CHANGE_TYPE_CHOICES = (
    ('C', 'Created'),
    ('U', 'Updated'),
    ('D', 'Canceled'),
)
class EventChangeLog(models.Model):
    event = models.ForeignKey(Event)
    change_type = models.CharField(max_length=1, choices=CHANGE_TYPE_CHOICES)
    date_time = models.DateTimeField(auto_now_add=True)
    
    @receiver(signals.post_save, sender=Event, dispatch_uid="EventChangeLog")
    def signal_receiver(sender, **kwargs):
        '''
        Creates a change log whenever an Event is created or updated
        '''
        event = kwargs['instance']
        
        ecl = EventChangeLog()
        ecl.event = event
        
        createTimestamp = time.mktime(event.get_date_time_created_utc().timetuple())
        modifyTimestamp = time.mktime(event.get_date_time_modified_utc().timetuple())
        if ( modifyTimestamp - createTimestamp ) < 1:
            ecl.change_type = 'C'
        elif event.canceled:
            ecl.change_type = 'D'
        else:
            ecl.change_type = 'U'
        
        ecl.save()

class StaticPage(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    content = models.TextField()
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)

class Setting(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    value = models.CharField(max_length=500)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)

class TweetedEvent(models.Model):
    event = models.ForeignKey(Event)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)
    



