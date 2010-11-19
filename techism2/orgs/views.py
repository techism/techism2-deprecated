#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from techism2.orgs import org_service

def index(request):
    tags = org_service.get_tags()
    return render_to_response('orgs/index.html', { 'tags': tags}, context_instance=RequestContext(request))

def tag(request, tag_name):
    list = org_service.get_base_organization_query_set().filter(tags=tag_name)
    tags = org_service.get_tags()
    return render_to_response('orgs/index.html', {'organization_list': list, 'tags': tags, 'tag_name': tag_name}, context_instance=RequestContext(request))

