from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from techism2.rss.feeds import UpcommingEventsRssFeed, UpcommingEventsAtomFeed
from techism2.sitemaps import TechismSitemap
from techism2.events.sitemaps import EventIndexSitemap, EventDetailsSitemap, EventTagsSitemap
from techism2.orgs.sitemaps import OrgIndexSitemap, OrgTagsSitemap

admin.autodiscover()

sitemaps = {
    'techism': TechismSitemap,
    'event_index': EventIndexSitemap,
    'event_details': EventDetailsSitemap,
    'event_tags': EventTagsSitemap,
    'org_index': OrgIndexSitemap,
    'org_tags': OrgTagsSitemap,
}

urlpatterns = patterns('',
    # events
    (r'^$', 'techism2.events.views.index'),
    (r'^events/$', 'techism2.events.views.index'),
    (r'^events/edit/(?P<event_id>\d+)/$', 'techism2.events.views.edit'),
    (r'^events/cancel/(?P<event_id>\d+)/$', 'techism2.events.views.cancel'),
    (r'^events/create/(?P<event_id>\d+)/$', 'techism2.events.views.create'),
    (r'^events/create/$', 'techism2.events.views.create'),
    (r'^events/archive/$', 'techism2.events.views.archive'),
    (r'^events/tags/(?P<tag_name>.+)/$', 'techism2.events.views.tag'),
    (r'^events/locations/$', 'techism2.events.views.locations'),
    (r'^events/(?P<event_id>.+)/$', 'techism2.events.views.details'),
    
    # orgs
    (r'^orgs/$', 'techism2.orgs.views.index'),
    (r'^orgs/tags/(?P<tag_name>.+)/$', 'techism2.orgs.views.tag'),
    
    # static pages
    (r'^impressum/$', 'techism2.views.static_impressum'),
    (r'^about/$', 'techism2.views.static_about'),
    
    # sitemap.xml
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    
    # iCal
    (r'^feed.ics$', 'techism2.ical.views.ical'),
    (r'^ical/(?P<event_id>.+).ics$', 'techism2.ical.views.ical_single_event'),
    
    # Atom
    (r'^feeds/atom/upcomming_events$', UpcommingEventsAtomFeed()),
    
    #RSS
    (r'^feeds/rss/upcomming_events$', UpcommingEventsRssFeed()),
    
    # admin
    (r'^admin/', include(admin.site.urls)),
    
    # login/logout
    (r'^accounts/', include('django_openid_auth.urls')),
    (r'^accounts/logout/$', 'techism2.views.logout'),
    url(r'^accounts/google_login/$', 'gaeauth.views.login', name='google_login'),
    url(r'^accounts/google_logout/$', 'gaeauth.views.logout', name='google_logout'),
    url(r'^accounts/google_authenticate/$', 'gaeauth.views.authenticate', name='google_authenticate'),
    
    # cron jobs
    (r'^cron/update_archived_flag', 'techism2.cron.views.update_archived_flag'),
    (r'^cron/update_organization_tags_cache', 'techism2.cron.views.update_organization_tags_cache'),
    (r'^cron/update_event_tags_cache', 'techism2.cron.views.update_event_tags_cache'),
    (r'^cron/tweet_upcoming_events', 'techism2.cron.twitter.tweet_upcoming_events'),
    ('^keepalive/$', direct_to_template, { 'template': 'keepalive.html' }),

)
