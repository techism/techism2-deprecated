#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism2 import service
from django.core.mail import send_mail
from django.core.cache import cache
from techism2 import service

tags_cache_key = "event_tags"

def get_tags(tags_cache_key):
    # Note: no synchronization, propably not possible on GAE
    tags = cache.get(tags_cache_key)
    if tags:
        return tags
    else:
        tags = update_tags_cache()
        return tags


def update_tags_cache():
    dict_list = service.get_event_query_set().values('tags')
    tags = service.fetch_tags(dict_list)
    cache.set(tags_cache_key, tags, 1800) # expire after 30 min
    return tags

def send_event_review_mail(event):
    subject = u'[Techism] Neues Event - bitte prüfen'
    message_details = u'Titel: %s\n\nBeschreibung: %s\n\n' % (event.title, event.description);
    message_urls = u'Login-Url: %s\n\nEvent-Url: %s\n\n' % (service.get_secure_url()+"/accounts/login/", service.get_secure_url()+"/admin/techism2/event/");
    message = message_details + message_urls
    fr = service.get_setting('event_review_mail_from')
    to = service.get_setting('event_review_mail_to').split(',')
    send_mail(subject, message, fr, to, fail_silently=False)