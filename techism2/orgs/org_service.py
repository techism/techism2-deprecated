#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism2.models import Organization
from techism2 import service

tags_cache_key = "organization_tags"

def get_tags():
    return service.get_tags(tags_cache_key, get_base_organization_query_set)

def update_tags_cache():
    service.update_tags_cache(tags_cache_key, get_base_organization_query_set)

def get_base_organization_query_set():
    return Organization.objects.all()
