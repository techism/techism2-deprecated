from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from techism2 import service
from techism2.events import event_service
from techism2.models import TweetedEvent, EventChangeLog
from datetime import datetime, timedelta
import tweepy
from tweepy.error import TweepError
import urllib
import logging

def tweet_upcoming_events(request):
    today = datetime.utcnow() + timedelta(days=0)
    three_days = datetime.utcnow() + timedelta(days=3)
    event_list = event_service.get_event_query_set().filter(date_time_begin__gte=today).filter(date_time_begin__lte=three_days).order_by('date_time_begin')
    
    for event in event_list:
        must_tweet, prefix = __must_tweet_and_prefix(event)
        if must_tweet:
            tweet = __format_tweet(event, prefix)
            try:
                __tweet_event(tweet)
                __mark_as_tweeted(event, tweet)
                break
            except TweepError, e:
                logging.error(e.reason)
                if e.reason == u'Status is a duplicate.':
                    __mark_as_tweeted(event, 'TweepError: Status is a duplicate.')
                    break
                else:
                    raise e
    response = HttpResponse()
    return response

def __must_tweet_and_prefix(event):
    # get last tweet
    tweet = None
    tweet_list = TweetedEvent.objects.filter(event=event).order_by('-date_time_created')
    if tweet_list.exists():
        tweet = tweet_list[0]
    
    # determine if we must tweet and the used prefix
    if event.canceled:
        if tweet is None or not tweet.tweet.startswith('[Abgesagt] '):
            return (True, '[Abgesagt] ')
    else:
        if tweet is None:
            return (True, '')
        elif not tweet.tweet.startswith('[Update] '):
            cl_list = EventChangeLog.objects.filter(event=event).filter(date_time__gte=tweet.date_time_created).order_by('-date_time')
            if cl_list.exists():
                return (True, '[Update] ')
    
    return (False, '')

def __format_tweet(event, prefix):
    if event.takes_more_than_one_day():
        date_string = event.get_date_time_begin_cet().strftime("%d.%m.%Y") + "-" + event.get_date_time_end_cet().strftime("%d.%m.%Y")
    else:
        date_string = event.get_date_time_begin_cet().strftime("%d.%m.%Y %H:%M")
    
    base_url = service.get_default_url()
    relative_url = reverse('event-show', args=[event.id])
    long_url = base_url + relative_url
    short_url = __shorten_url(long_url)
    
    max_length = 140 - len(date_string) - len(short_url) - len(prefix) - 5
    title = event.title[:max_length]
    
    tweet = u'%s%s - %s %s' % (prefix, title, date_string, short_url)
    
    return tweet

def __shorten_url(url):
    for attempt in range(1, 10):
        f = None
        try:
            params = urllib.urlencode({'security_token': None, 'url': url})
            f = urllib.urlopen('http://goo.gl/api/shorten', params)
            short_url = json.loads(f.read())['short_url']
            return short_url
        except ValueError, error:
            pass
        finally:
            if f is not None:
                f.close()
    raise error

def __tweet_event(tweet):
    CONSUMER_KEY = service.get_setting('twitter_consumer_key')
    CONSUMER_SECRET = service.get_setting('twitter_consumer_secret')
    ACCESS_KEY = service.get_setting('twitter_access_key')
    ACCESS_SECRET = service.get_setting('twitter_access_secret')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status(tweet)

def __mark_as_tweeted(event, tweet):
    tweeted_event = TweetedEvent()
    tweeted_event.event = event
    tweeted_event.tweet = tweet
    tweeted_event.save()

