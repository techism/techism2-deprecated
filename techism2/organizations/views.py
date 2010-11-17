#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from techism2.models import Organization
from techism2.organizations import org_service

def index(request):
    #list = Organization.objects.all()
    tags = org_service.get_tags()
    #return render_to_response('organizations/index.html', {'organization_list': list, 'tags': tags}, context_instance=RequestContext(request))
    return render_to_response('organizations/index.html', { 'tags': tags}, context_instance=RequestContext(request))

def tag(request, tag_name):
    list = Organization.objects.all().filter(tags=tag_name)
    tags = org_service.get_tags()
    return render_to_response('organizations/index.html', {'organization_list': list, 'tags': tags, 'tag_name': tag_name}, context_instance=RequestContext(request))

