#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism2.models import Event, Setting
from django.core.cache import cache
from django.core.mail import send_mail

tags_cache_key = "event_tags"


def get_event_query_set():
    "Gets a base query set with all non-archived and published events"
    return __get_base_event_query_set().filter(archived__exact=False)

def get_archived_event_query_set():
    "Gets a base query set with all archived and published events"
    return __get_base_event_query_set().filter(archived__exact=True)

def __get_base_event_query_set():
    return Event.objects.filter(published__exact=True)

def get_tags():
    # Note: no synchronization, propably not possible on GAE
    tags = cache.get(tags_cache_key)
    
    if tags:
        return tags
    else:
        tags = update_tags_cache()
        return tags

def update_tags_cache():
    dict_list = get_event_query_set().values('tags')
    tags = fetch_tags(dict_list)
    cache.set(tags_cache_key, tags, 1800) # expire after 30 min
    return tags

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

def send_event_review_mail(event):
    subject = u'[Techism] Neues Event - bitte prüfen'
    message_details = u'Titel: %s\n\nBeschreibung: %s\n\n' % (event.title, event.description);
    message_urls = u'Login-Url: %s\n\nEvent-Url: %s\n\n' % (get_secure_url()+"/accounts/login/", get_secure_url()+"/admin/techism2/event/");
    message = message_details + message_urls
    fr = get_setting('event_review_mail_from')
    to = get_setting('event_review_mail_to').split(',')
    send_mail(subject, message, fr, to, fail_silently=False)

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

