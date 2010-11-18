#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism2.models import Event, Setting
from django.core.cache import cache
from django.core.mail import send_mail


def get_tags(tags_cache_key, fn):
    # Note: no synchronization, propably not possible on GAE
    tags = cache.get(tags_cache_key)
    
    if tags:
        return tags
    else:
        tags = update_tags_cache(tags_cache_key, fn)
        return tags

def update_tags_cache(tags_cache_key, fn):
    dict_list = fn().values('tags')
    tags = fetch_tags(dict_list)
    cache.set(tags_cache_key, tags, 1) # expire after 30 min
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
    
    # create tag list, each list item is a dict containing tag name and count
    tag_list = []
    for name,count in tags.items():
        tag_list.append({'name':name,'count':count})
    
    # calculate weigth for each tag
    tag_list = sorted(tag_list, key=lambda k: k['count'])
    lb = tag_list[0]['count']
    ub = tag_list[-1]['count']
    quotient = float(ub - lb + 1) / 9
    for tag in tag_list:
        tag['weigth'] = int(tag['count'] / quotient)
    
    return tag_list

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

