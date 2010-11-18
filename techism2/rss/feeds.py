#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from techism2.events import event_service
from techism2.models import EventChangeLog, ChangeType

 

class UpcommingEventsRssFeed(Feed):
    title = "Techism"
    link = "/events/"
    description = "Techism - Events, Projekte, Usergroups in München"

    def items(self):
        return event_service.get_event_query_set().order_by('date_time_begin')

    def item_title(self, item):
        prefix = self.__get_prefix(item)
        if item.takes_more_than_one_day():
            dateString = item.get_date_time_begin_cet().strftime("%d.%m.%Y") + "-" + item.get_date_time_end_cet().strftime("%d.%m.%Y")
        else:
            dateString = item.get_date_time_begin_cet().strftime("%d.%m.%Y %H:%M")
        return prefix + item.title + " - " + dateString

    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return "/events/" + str(item.id)
    
    def __get_prefix(self, event):
        prefix = ""
        
        if event.canceled:
            prefix = "[Abgesagt] ";
        else:
            change_log_items = EventChangeLog.objects.filter(event=event).filter(change_type=ChangeType.UPDATED).order_by('date_time')
            if change_log_items.exists():
                change_type = change_log_items[0].change_type
                if change_type == ChangeType.UPDATED:
                    if change_log_items.count() > 1:
                        prefix = "[Update %s] " % str(change_log_items.count());
                    else:
                        prefix = "[Update] ";
        
        return prefix

class UpcommingEventsAtomFeed(UpcommingEventsRssFeed):
    feed_type = Atom1Feed


