#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.core.cache import cache
from techism2.models import Organization

tags_cache_key = "organization_tags"

def update_tags_cache():
    tags = __fetch_tags()
    cache.set(tags_cache_key, tags, 1800) # expire after 30 min
    return tags

def __fetch_tags():
    dict_list = __get_base_organization_query_set().values('tags')
    tags = dict()    
    for dictionary in dict_list:
        for tag_list in dictionary.itervalues():
            if tag_list:
                for tag in tag_list:
                    if tag not in tags:
                        tags[tag] = 0
                    tags[tag] += 1
    return tags

def __get_base_organization_query_set():
    return Organization.objects.all()