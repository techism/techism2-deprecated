#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism2.models import EventChangeLog, ChangeType


def get_change_log_prefix(event):
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
