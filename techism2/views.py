#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from techism2.models import StaticPage
from django.contrib.auth import logout as django_logout


def static_impressum(request):
    return __render_static_page(request, 'static.impressum')

def static_about(request):
    return __render_static_page(request, 'static.about')

def __render_static_page(request, name):
    page, created = StaticPage.objects.get_or_create(name=name, defaults={'content': u'<section id="content">Bitte Inhalt einf\u00FCgen.</section>'})
    return render_to_response('static.html', {'content': page.content}, context_instance=RequestContext(request))

def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')

