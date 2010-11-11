#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from techism2.models import Organization
from techism2.organizations import org_service

tags_cache_key = "organization_tags"

def index(request):
    list = Organization.objects.all()
    tags = org_service.get_tags(tags_cache_key)
    return render_to_response('organizations/index.html', {'organization_list': list, 'tags': tags}, context_instance=RequestContext(request))
