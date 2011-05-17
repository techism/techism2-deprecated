#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound, HttpResponse
from techism2.models import Event, Location
from techism2.events.forms import EventForm, EventCancelForm
from techism2.events import event_service
from techism2 import service
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import simplejson as json
from django.utils import html


def index(request):
    event_list = event_service.get_event_query_set().order_by('date_time_begin')
    tags = event_service.get_tags()
    page = __get_paginator_page(request, event_list)
    if page == -1:
        return HttpResponseNotFound()
    return render_to_response('events/index.html', {'event_list': page, 'tags': tags}, context_instance=RequestContext(request))

def archive(request):
    event_list = event_service.get_archived_event_query_set().order_by('-date_time_begin')
    tags = event_service.get_tags()
    page = __get_paginator_page(request, event_list)
    if page == -1:
        return HttpResponseNotFound()
    return render_to_response('events/index.html', {'event_list': page, 'tags': tags}, context_instance=RequestContext(request))

def tag(request, tag_name):
    event_list = event_service.get_event_query_set().filter(tags=tag_name).order_by('date_time_begin')
    tags = event_service.get_tags()
    page = __get_paginator_page(request, event_list)
    if page == -1:
        return HttpResponseNotFound()
    return render_to_response('events/index.html', {'event_list': page, 'tags': tags, 'tag_name': tag_name}, context_instance=RequestContext(request))

def create(request, event_id=None):
    button_label = u'Event hinzuf\u00FCgen'
    locations_as_json = __get_locations_as_json()
    
    if request.method == 'POST':
        return __save_event(request, button_label, locations_as_json)
    
    form = EventForm()
    if event_id:
        event = Event.objects.get(id=event_id)
        form = __to_event_form(event)
    
    return render_to_response(
        'events/create.html',
        {
            'form': form,
            'button_label': button_label
        },
        context_instance=RequestContext(request))


def cancel(request, event_id):
    event = Event.objects.get(id=event_id)
    
    if request.method == 'POST':
        return __cancel_event(request, event)
    
    return render_to_response(
        'events/cancel.html',
        {
            'form:': EventCancelForm(),
            'event': event
        },
        context_instance=RequestContext(request))


def edit(request, event_id):
    button_label = u'Event \u00E4ndern'
    locations_as_json = __get_locations_as_json()
    
    event = Event.objects.get(id=event_id)
    if event.user != request.user and request.user.is_superuser == False:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        return __save_event(request, button_label, locations_as_json, event)
    
    form = __to_event_form(event)
    return render_to_response(
        'events/create.html',
        {
            'form': form,
            'button_label': button_label
        },
        context_instance=RequestContext(request))


def details(request, event_id):
    # the event_id may be the slugified, e.g. 'munichjs-meetup-286002'
    splitted_event_id = event_id.rsplit('-', 1)
    if len(splitted_event_id) > 1:
        event_id = splitted_event_id[1]
    
    tags = event_service.get_tags()
    event = Event.objects.get(id=event_id)
    return render_to_response(
        'events/details.html',
        {
            'event': event,
            'tags': tags
        },
        context_instance=RequestContext(request))

def __cancel_event(request, event):
    form = EventCancelForm(request.POST) 
    if form.is_valid():
        event.canceled = True;
        event.save()
        url = event.get_absolute_url()
        return HttpResponseRedirect(url)
    else:
        return render_to_response(
        'events/cancel.html',
        {
            'form:': form,
            'error': form.errors,
            'event': event
        },
        context_instance=RequestContext(request))
        
def locations(request):
    return HttpResponse(__get_locations_as_json())
    

def __save_event(request, button_label, locations_as_json, old_event=None):
    form = EventForm(request.POST) 
    if form.is_valid(): 
        event= __create_or_update_event_with_location(form, request.user, old_event)
        #if not event.published:
            #service.send_event_review_mail(event)
        url = event.get_absolute_url()
        return HttpResponseRedirect(url)
    else:
        return render_to_response(
            'events/create.html',
            {
                'form': form, 
                'error': form.errors,
                'button_label': button_label
            },
            context_instance=RequestContext(request))

def __create_or_update_event_with_location (form, user, event):
    "Creates or updates an Event from the submitted EventForm. If the given Event is None a new Event is created."
    if event == None:
        event = Event()
    
    event.title=form.cleaned_data['title']
    event.set_date_time_begin_cet(form.cleaned_data['date_time_begin'])
    event.set_date_time_end_cet(form.cleaned_data['date_time_end'])
    event.url=form.cleaned_data['url']
    event.description=form.cleaned_data['description']
    event.location=form.cleaned_data['location']
    event.tags=form.cleaned_data['tags']
    
    if event.location == None:
        location = __create_location(form)
        event.location=location
    
    # Only when a new event is created
    if event.id == None:
        # auto-publish for staff users
        event.published = user.is_staff
        # link event to user
        if user.is_authenticated():
            event.user=user
    
    # Compute and store the archived flag
    event.update_archived_flag()
    
    event.save()
    
    return event

def __create_location (form):
    "Creates a Location from the submitted EventForm"
    location = Location()
    location.name=form.cleaned_data['location_name']
    location.street=form.cleaned_data['location_street']
    location.city=form.cleaned_data['location_city']
    if location.name and location.street and location.city:
        location.save()
        return location
    else:
        return None

def __to_event_form (event):
    "Converts an Event to an EventForm"
    data = {'title': event.title,
            'date_time_begin': event.get_date_time_begin_cet(),
            'date_time_begin_0': event.get_date_time_begin_cet(),
            'date_time_begin_1': event.get_date_time_begin_cet(),
            'date_time_end': event.get_date_time_end_cet(),
            'date_time_end_0': event.get_date_time_end_cet(),
            'date_time_end_1': event.get_date_time_end_cet(),
            'url': event.url,
            'description': event.description,
            'location': event.location.id if event.location else None,
            'tags': event.tags,
            #'location_name': event.location.name,
            #'location_street': event.location.street,
            #'location_city': event.location.city
            }
    form = EventForm(data)
    return form;

def __get_paginator_page(request, event_list):
    try:
        num = int(request.GET.get('page', '1'))
    except ValueError:
        num = 1
    
    paginator = Paginator(event_list, 7);
    try:
        page = paginator.page(num)
    except (EmptyPage, InvalidPage):
        page = -1
    
    return page

def __get_locations_as_json():
    location_list = Location.objects.all()
    locations = []
    for location in location_list:
        loc = dict()
        loc['id'] = html.escape(location.id)
        loc['name'] = html.escape(location.name)
        loc['street'] = html.escape(location.street)
        loc['city'] = html.escape(location.city)
        locations.append(loc)
    locations_as_json = json.dumps(locations)
    return locations_as_json

