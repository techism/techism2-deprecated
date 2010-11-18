#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism2.models import Event
from techism2 import service

tags_cache_key = "event_tags"

def get_tags():
    return service.get_tags(tags_cache_key, get_event_query_set)

def update_tags_cache():
    service.update_tags_cache(tags_cache_key, get_event_query_set)

def __get_base_event_query_set():
    return Event.objects.filter(published__exact=True)

def get_event_query_set():
    "Gets a base query set with all non-archived and published events"
    return __get_base_event_query_set().filter(archived__exact=False)

def get_archived_event_query_set():
    "Gets a base query set with all archived and published events"
    return __get_base_event_query_set().filter(archived__exact=True)
