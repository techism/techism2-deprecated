#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from techism2.rss import utils
from techism2.events import event_service


class UpcommingEventsRssFeed(Feed):
    title = "Techism"
    link = "/events/"
    description = "Techism - Events, Projekte, Usergroups in München"

    def items(self):
        return event_service.get_event_query_set().order_by('date_time_begin')

    def item_title(self, item):
        prefix = utils.get_change_log_prefix(item)
        if item.takes_more_than_one_day():
            dateString = item.get_date_time_begin_cet().strftime("%d.%m.%Y") + "-" + item.get_date_time_end_cet().strftime("%d.%m.%Y")
        else:
            dateString = item.get_date_time_begin_cet().strftime("%d.%m.%Y %H:%M")
        return prefix + item.title + " - " + dateString

    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return "/events/" + str(item.id)
    
    def author_name(self):
        return "Techism"
    
    def item_pubdate(self, item):
        return item.date_time_modified

class UpcommingEventsAtomFeed(UpcommingEventsRssFeed):
    feed_type = Atom1Feed


