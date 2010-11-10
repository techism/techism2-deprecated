#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from techism2.models import Organization

def index(request):
    list = Organization.objects.all()
    return render_to_response('organizations/index.html', {'organization_list': list}, context_instance=RequestContext(request))
