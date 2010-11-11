#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism2.models import Setting, Event
from django.core.cache import cache

def get_event_query_set():
    "Gets a base query set with all non-archived and published events"
    return __get_base_event_query_set().filter(archived__exact=False)

def get_archived_event_query_set():
    "Gets a base query set with all archived and published events"
    return __get_base_event_query_set().filter(archived__exact=True)

def __get_base_event_query_set():
    return Event.objects.filter(published__exact=True)
def fetch_tags(dict_list):
    tags = dict()    
    for dictionary in dict_list:
        for tag_list in dictionary.itervalues():
            if tag_list:
                for tag in tag_list:
                    if tag not in tags:
                        tags[tag] = 0
                    tags[tag] += 1
    return tags

def get_secret_key():
    return get_setting('SECRET_KEY')

def get_secure_url():
    return get_setting('secure_url')

def get_default_url():
    return get_setting('default_url')

def get_setting(name):
    setting, _ = Setting.objects.get_or_create(name=name, defaults={'value': u'none'})
    value = setting.value
    return value

